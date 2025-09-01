from escpos.printer import Usb
from datetime import datetime, timedelta

claim_minutes = 15  # Adjust this value as needed
restock_time = (datetime.now() + timedelta(minutes=claim_minutes)).strftime("%I:%M %p")

vendor_id = 0x076c
product_id = 0x0302

printer = Usb(vendor_id, product_id, interface=0, out_ep=0x02, in_ep=0x82)


# Print logo (centered)
# printer.set(align='center' )
# printer.image("./pc-logo.png")  # Replace with your actual file name
# printer.textln(" ")
# printer.textln(" ")


def print_ticket(customer_name, costume_number, costume_size):

    # Title: Large, bold, centered
    printer.set(align='center', bold=True, font='a', width=4, height=4)
    printer.textln("Party City Halloween Store!")
    printer.textln(" ")
    printer.textln(" ")
    printer.text("\n")

 
    # Details: Normal size, left aligned
    printer.set(align='left', bold=False, width=1, height=1)
    printer.textln(f"Name: {customer_name}")
    printer.textln(f"Costume #: {costume_number}")
    printer.textln(f"Size: {costume_size.upper()}")
    printer.textln(" ")
    printer.textln(" ")
    printer.text("\n\n")

    # Note: Slightly smaller (Font B), left aligned
    printer.set(align='center', bold=False, font='b', width=1, height=1)
    printer.textln(f"Note: You have {claim_minutes} minutes to claim")
    printer.textln("your costume before it's restocking.")
    printer.textln(f"Restock Time: {restock_time}")
    printer.textln(" ")
    printer.text("\n\n\n")

    # Signature line, centered
    printer.set(align='center', bold=False, width=1, height=1)
    printer.textln("_______________________________________________________________")
    printer.textln("Signature")
    printer.textln(" ")
    printer.textln(" ")
    printer.cut()
