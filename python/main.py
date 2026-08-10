import tkinter as tk
from tkinter import messagebox
import cv2
import requests
from datetime import datetime
import urllib3
import threading

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --------------------------
# CONFIGURATION
# --------------------------
API_URL_PUT = "https://oracleapex.com/ords/dm20/myapi/putdata"
API_URL_GET = "https://oracleapex.com/ords/dm20/myapi/getdata"
USERNAME = "4397146@myuwc.ac.za"
PASSWORD = "Apex_Dhruvi04"

# Global variables
employee_id = None
booking_id = None

# --------------------------
# QR SCANNING FUNCTION USING CV2
# --------------------------
def scan_qr_from_camera():
    """
    Opens the camera and scans for a QR code using OpenCV.
    Returns the data from the QR code or None if cancelled.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Cannot access camera")
        return None

    detector = cv2.QRCodeDetector()
    print("Scanning QR code... Press 'q' to cancel.")
    scanned_data = None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            scanned_data = data
            cap.release()
            cv2.destroyAllWindows()
            return scanned_data

        cv2.imshow("Scan QR Code (press 'q' to cancel)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

# --------------------------
# API FUNCTIONS
# --------------------------
def submit_checkin(employee_id, booking_id):
    """
    Submit the check-in request to update the booking with return date
    """
    try:
        timeout = 30
        payload = {
            "employee_id": employee_id, 
            "booking_id": booking_id,
            "date_returned": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        print(f"Sending PUT request to {API_URL_PUT}")
        print(f"Payload: {payload}")

        response_put = requests.put(
            API_URL_PUT,
            json=payload,
            auth=(USERNAME, PASSWORD),
            timeout=timeout,
            verify=False,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Equipment-Checkin-App/1.0'
            }
        )

        print(f"PUT Response Status: {response_put.status_code}")
        print(f"PUT Response: {response_put.text}")
        response_put.raise_for_status()

        try:
            result_put = response_put.json()
        except ValueError:
            root.after(0, lambda: messagebox.showerror("Error", "Invalid response from server"))
            return

        if result_put.get("status") == "success":
            print(f"Success: Item checked in (Booking ID: {booking_id})")
            root.after(0, lambda: messagebox.showinfo("Success", 
                f"Equipment returned successfully!\nBooking ID: {booking_id}\nEmployee ID: {employee_id}"))
            
            # Clear the booking entry for next use
            root.after(0, lambda: booking_entry.delete(0, tk.END))
            
        else:
            error_msg = result_put.get('message', 'Unknown error during check-in')
            print(f"Error: {error_msg}")
            root.after(0, lambda: messagebox.showerror("Error", f"Failed to return equipment:\n{error_msg}"))

    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
        root.after(0, lambda: messagebox.showerror("Error", "Request timed out. Please try again."))
    except requests.exceptions.ConnectionError as e:
        print(f"Error: Connection error: {str(e)}")
        root.after(0, lambda: messagebox.showerror("Error", f"Connection error: {str(e)}"))
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error: {str(e)}")
        root.after(0, lambda: messagebox.showerror("Error", f"HTTP error: {str(e)}"))
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        root.after(0, lambda: messagebox.showerror("Error", f"Unexpected error: {str(e)}"))

def checkin_booking(booking_id, employee_id):
    """
    Handle the check-in process with threading to avoid UI freezing
    """
    global submit_btn
    
    if not employee_id or not booking_id:
        messagebox.showerror("Error", "Missing booking ID or employee ID")
        return False, "Missing required information"
    
    # Disable button during processing
    submit_btn.config(state='disabled', text='Processing...')

    def checkin_worker():
        try:
            submit_checkin(employee_id, booking_id)
        finally:
            root.after(0, lambda: submit_btn.config(state='normal', text='Submit & Scan QR'))

    thread = threading.Thread(target=checkin_worker, daemon=True)
    thread.start()
    
    return True, "Processing started"

# --------------------------
# TKINTER CALLBACK
# --------------------------
def submit_booking():
    """
    Main function to handle booking submission and QR scanning
    """
    global booking_id, employee_id
    
    # Get booking ID from entry
    booking_id = booking_entry.get().strip()
    if not booking_id:
        messagebox.showwarning("Input Required", "Please enter a Booking ID.")
        booking_entry.focus()
        return

    print(f"Booking ID entered: {booking_id}")
    
    # Scan QR code for employee ID
    qr_data = scan_qr_from_camera()
    if qr_data:
        employee_id = qr_data.strip()
        print(f"Scanned QR code data (Employee ID): {employee_id}")
        
        # Process the check-in
        success, response = checkin_booking(booking_id, employee_id)
        if not success:
            messagebox.showerror("Error", f"Failed to process return:\n{response}")
    else:
        print("No QR code scanned or operation cancelled.")
        messagebox.showinfo("Cancelled", "QR code scanning was cancelled.")

# --------------------------
# TKINTER GUI
# --------------------------
root = tk.Tk()
root.title("Return Equipment - QR Scanner")
root.geometry("450x300")
root.configure(bg='#f0f0f0')

# Center the window
root.eval('tk::PlaceWindow . center')

# Create main frame
main_frame = tk.Frame(root, bg='#f0f0f0')
main_frame.pack(expand=True, fill='both', padx=20, pady=20)

# Input frame
center_frame = tk.Frame(main_frame, bg='#f0f0f0')
center_frame.pack(expand=True)

tk.Label(center_frame, text="Enter Booking ID:", font=("Arial", 12), bg='#f0f0f0').pack(pady=10)
booking_entry = tk.Entry(center_frame, width=25, font=("Arial", 12), justify='center')
booking_entry.pack(pady=10)

submit_btn = tk.Button(
    center_frame, 
    text="Submit & Scan QR", 
    command=submit_booking,
    font=("Arial", 11),
    fg='black',
    padx=20,
    pady=10
)
submit_btn.pack(pady=20)

# Allow Enter key to trigger submission
booking_entry.bind('<Return>', lambda event: submit_booking())

# Focus on the entry field
booking_entry.focus()

# Handle window close
def on_closing():
    # Close any open CV2 windows
    cv2.destroyAllWindows()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
