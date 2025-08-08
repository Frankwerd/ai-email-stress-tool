# main.py

# --- MODIFIED: Import ttkbootstrap instead of tkinter ---
import ttkbootstrap as ttk
from ttkbootstrap.constants import * # Imports constants like LEFT, NORMAL, DISABLED
# We still need the original tkinter for modules that ttkbootstrap doesn't replace
from tkinter import messagebox, filedialog 
import threading
import time
import webbrowser

# Import your other modules
from ai_content import generate_email_content
from email_sender import send_email

# --- Global variable to control the sending thread ---
cancel_sending_event = threading.Event()

def open_link(url):
    """Opens the provided URL in a new browser tab."""
    webbrowser.open_new_tab(url)

def start_email_thread():
    """
    Starts the email-sending process in a new thread to keep the GUI from freezing.
    """
    start_button.config(state=DISABLED) # Use constant from ttkbootstrap
    cancel_button.config(state=NORMAL)
    cancel_sending_event.clear()

    params = {
        "sender": entry_email.get(), "password": entry_password.get(),
        "api_key": entry_api_key.get(), "recipient": entry_recipient.get(),
        "cc_recipients_str": entry_cc.get(), "bcc_recipients_str": entry_bcc.get(),
        "num_emails_str": entry_num_emails.get(), "delay_str": entry_delay.get(),
        "purpose": entry_purpose.get(), "tone": entry_tone.get(),
        "email_format": format_var.get(), "attachment_path": attachment_path_var.get()
    }
    
    email_thread = threading.Thread(target=handle_send_emails, args=(params,))
    email_thread.start()

def cancel_sending():
    """Sets the event flag to signal the sending thread to stop."""
    if messagebox.askyesno("Cancel?", "Are you sure you want to stop sending emails?"):
        print("\n--- CANCELLATION SIGNAL SENT ---")
        cancel_sending_event.set()

def handle_send_emails(params: dict):
    """
    This function runs in a separate thread and performs the actual work.
    (This function's internal logic does not need to change)
    """
    try:
        if not all([params["sender"], params["password"], params["api_key"], params["recipient"], params["num_emails_str"]]):
            messagebox.showerror("Error", "Core fields (Auth, Recipient, Number of Emails) are required!")
            return

        num_emails = int(params["num_emails_str"])
        delay = int(params["delay_str"] or "5")
        cc_list = [email.strip() for email in params["cc_recipients_str"].split(',') if email.strip()]
        bcc_list = [email.strip() for email in params["bcc_recipients_str"].split(',') if email.strip()]

        print("--- PROCESS STARTED ---")
        emails_sent_count = 0

        for i in range(num_emails):
            if cancel_sending_event.is_set():
                print("Cancellation detected. Stopping the email loop.")
                break

            print(f"\n--- Preparing Email {i + 1} of {num_emails} ---")
            print("1. Generating AI content...")
            ai_result = generate_email_content(params["api_key"], params["purpose"], params["tone"])
            
            if ai_result:
                print("   -> AI content generated successfully.")
                success = send_email(
                    sender_email=params["sender"], app_password=params["password"],
                    receiver_email=params["recipient"], cc_list=cc_list, bcc_list=bcc_list,
                    subject=ai_result['subject'], body=ai_result['body'],
                    email_format=params["email_format"], attachment_path=params["attachment_path"]
                )
                if success: emails_sent_count += 1
            else:
                print("   -> FAILED to generate AI content. Skipping email.")

            if i < num_emails - 1:
                print(f"3. Waiting for {delay} seconds...")
                if cancel_sending_event.wait(timeout=delay):
                    print("Cancellation detected during delay.")
                    break

        print(f"\n--- PROCESS COMPLETE ---")
        if cancel_sending_event.is_set():
            messagebox.showinfo("Process Cancelled", f"Process was stopped. Sent {emails_sent_count} emails.")
        else:
            messagebox.showinfo("Process Complete", f"Finished. Sent {emails_sent_count} out of {num_emails} emails.")

    except ValueError:
        messagebox.showerror("Input Error", "Please ensure 'Number of emails' and 'Delay' are valid numbers.")
    except Exception as e:
        messagebox.showerror("An Error Occurred", f"An unexpected error occurred:\n{e}")
    finally:
        start_button.config(state=NORMAL)
        cancel_button.config(state=DISABLED)

def browse_file():
    """Opens a file dialog to select an attachment."""
    filepath = filedialog.askopenfilename()
    if filepath:
        attachment_path_var.set(filepath)


# --- GUI SETUP ---
# --- MODIFIED: Create a themed window. Try other themes: "cyborg", "litera", "minty", "darkly" ---
window = ttk.Window(themename="superhero")
window.title("AI Stress-Testing Email Tool")

# Create frames for organization (using ttk.LabelFrame for a themed look)
auth_frame = ttk.LabelFrame(window, text="Authentication", padding=(10, 10))
auth_frame.pack(padx=10, pady=10, fill="x")

recipient_frame = ttk.LabelFrame(window, text="Recipients", padding=(10, 10))
recipient_frame.pack(padx=10, pady=10, fill="x")

content_frame = ttk.LabelFrame(window, text="Email Content & Behavior", padding=(10, 10))
content_frame.pack(padx=10, pady=10, fill="x")

action_frame = ttk.Frame(window, padding=(10, 10)) # Use a simple Frame here
action_frame.pack(padx=10, pady=5, fill="x")


# --- MODIFIED: All widgets are now from ttkbootstrap ---
# --- Authentication Widgets ---
ttk.Label(auth_frame, text="Your Gmail Address:").grid(row=0, column=0, sticky="w")
entry_email = ttk.Entry(auth_frame)
entry_email.grid(row=0, column=1, sticky="ew", padx=5)
auth_frame.grid_columnconfigure(1, weight=1) # Makes entry expand

ttk.Label(auth_frame, text="Your Gmail App Password:").grid(row=1, column=0, sticky="w")
entry_password = ttk.Entry(auth_frame, show="*")
entry_password.grid(row=1, column=1, sticky="ew", padx=5)

app_password_link = ttk.Label(auth_frame, text="Enable 2-Step Verification, then get password here.",
                              bootstyle="primary", cursor="hand2") # Use bootstyle for color
app_password_link.grid(row=2, column=1, sticky="w", padx=5, pady=(0, 10))
app_password_link.bind("<Button-1>", lambda e: open_link("https://myaccount.google.com/apppasswords"))

ttk.Label(auth_frame, text="Your Gemini API Key:").grid(row=3, column=0, sticky="w")
entry_api_key = ttk.Entry(auth_frame, show="*")
entry_api_key.grid(row=3, column=1, sticky="ew", padx=5)

# --- Recipient Widgets ---
ttk.Label(recipient_frame, text="To:").grid(row=0, column=0, sticky="w")
entry_recipient = ttk.Entry(recipient_frame)
entry_recipient.grid(row=0, column=1, sticky="ew", padx=5)
recipient_frame.grid_columnconfigure(1, weight=1)

ttk.Label(recipient_frame, text="Cc (comma-separated):").grid(row=1, column=0, sticky="w")
entry_cc = ttk.Entry(recipient_frame)
entry_cc.grid(row=1, column=1, sticky="ew", padx=5)

ttk.Label(recipient_frame, text="Bcc (comma-separated):").grid(row=2, column=0, sticky="w")
entry_bcc = ttk.Entry(recipient_frame)
entry_bcc.grid(row=2, column=1, sticky="ew", padx=5)

# --- Content Widgets ---
content_grid_frame = ttk.Frame(content_frame)
content_grid_frame.pack(fill="x")

ttk.Label(content_grid_frame, text="Number of emails:").grid(row=0, column=0, sticky="w")
entry_num_emails = ttk.Entry(content_grid_frame, width=10)
entry_num_emails.grid(row=0, column=1, sticky="w", padx=5)

ttk.Label(content_grid_frame, text="Delay (sec):").grid(row=0, column=2, sticky="w", padx=15)
entry_delay = ttk.Entry(content_grid_frame, width=10)
entry_delay.grid(row=0, column=3, sticky="w", padx=5)
entry_delay.insert(0, "5")

ttk.Label(content_grid_frame, text="AI Purpose:").grid(row=1, column=0, sticky="w", pady=(10,0))
entry_purpose = ttk.Entry(content_grid_frame)
entry_purpose.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=(10,0))

ttk.Label(content_grid_frame, text="AI Tone/Style:").grid(row=2, column=0, sticky="w", pady=(5,0))
entry_tone = ttk.Entry(content_grid_frame)
entry_tone.grid(row=2, column=1, columnspan=3, sticky="ew", padx=5, pady=(5,0))
entry_tone.insert(0, "Professional")

format_var = ttk.StringVar(value="plain")
ttk.Label(content_grid_frame, text="Format:").grid(row=3, column=0, sticky="w", pady=(5,0))
format_options_frame = ttk.Frame(content_grid_frame)
format_options_frame.grid(row=3, column=1, columnspan=3, sticky="w", padx=5, pady=(5,0))
# Style radiobuttons to look like buttons
ttk.Radiobutton(format_options_frame, text="Plain Text", variable=format_var, value="plain", bootstyle="toolbutton").pack(side=LEFT)
ttk.Radiobutton(format_options_frame, text="HTML", variable=format_var, value="html", bootstyle="toolbutton").pack(side=LEFT, padx=10)

attachment_path_var = ttk.StringVar()
ttk.Label(content_grid_frame, text="Attachment:").grid(row=4, column=0, sticky="w", pady=(5,0))
entry_attachment = ttk.Entry(content_grid_frame, textvariable=attachment_path_var, state=DISABLED)
entry_attachment.grid(row=4, column=1, columnspan=2, sticky="ew", padx=5, pady=(5,0))
ttk.Button(content_grid_frame, text="Browse...", command=browse_file, bootstyle="outline-secondary").grid(row=4, column=3, sticky="w", padx=5, pady=(5,0))
content_grid_frame.grid_columnconfigure(1, weight=1)

# --- Action Buttons ---
# --- MODIFIED: Use bootstyle for professional, consistent colors ---
start_button = ttk.Button(action_frame, text="Start Sending Emails", command=start_email_thread, bootstyle="success")
start_button.pack(side=LEFT, expand=True, fill="x", padx=5)

cancel_button = ttk.Button(action_frame, text="Cancel", command=cancel_sending, bootstyle="danger", state=DISABLED)
cancel_button.pack(side=LEFT, expand=True, fill="x", padx=5)

window.mainloop()