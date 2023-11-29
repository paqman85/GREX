from datetime import date
from datetime import datetime
from decimal import Decimal
from pony.orm import *


db = Database()


class Part(db.Entity):
    id = PrimaryKey(int, auto=True)
    number = Optional(str, unique=True)  # Part number property.
    desc = Optional(str)  # Part Description
    on_hand = Optional(int)  # The number of units in the warehouse.
    committed = Optional(int)  # Parts committed to orders or jobs.
    reserve = Optional(int)
    on_order = Optional(int)  # Number of units currently on order
    category = Required(str, default='Dana')
    do_not_sell = Optional(bool, default=False)  # Do not sell - True or False
    first_in = Optional(int)  # First In (inventory qty)
    first_in_cost = Optional(Decimal)  # Avg cost for first in
    mid_in = Optional(int)  # Mid In (inventory Qty)
    mid_in_cost = Optional(Decimal)  # Mid In avg cost
    last_in = Optional(int)  # Last In (inventory qty)
    last_in_cost = Optional(Decimal)  # Last In In avg cost
    average_cost = Optional(Decimal)  # Average Costs of all in stock items
    actual_cost = Optional(Decimal)  # Actual Cost (from list pricing)
    location_primary = Optional(str)  # Primary Location
    location_overstock = Optional(str)  # Overstock Location
    weight = Optional(Decimal)  # Weight in lbs
    application = Optional(LongStr)  # Application notes
    LastPrice = Optional(str)
    invoice_lines = Set('Invoice_line')
    p_o_lines = Set('PO_line')


class Currency(db.Entity):
    id = PrimaryKey(int, auto=True)
    Code = Required(str, unique=True)
    Desc = Required(str)  # Currency description
    CValue = Required(Decimal)  # Current system value
    LValue = Optional(Decimal)  # Previous value
    LDate = Optional(date)  # Last time value was changed.
    customers = Set('Customer')


class Customer(db.Entity):
    id = PrimaryKey(int, auto=True)
    code = Required(str)  # Customer code
    name = Optional(str)  # Customer Name
    b_addr = Required(LongStr)  # Billing Address
    tax = Required('Tax')
    shipping_addresses = Set('ShippingAddresse')
    currency = Required(Currency)
    sales = Set('Sale')


class Tax(db.Entity):
    id = PrimaryKey(int, auto=True)
    code = Required(str)
    abrev = Required(str)
    name = Required(str)
    rate = Required(str)
    description = Optional(str)
    customers = Set(Customer)


class ShippingAddresse(db.Entity):
    id = PrimaryKey(int, auto=True)
    Name = Required(str)
    address = Required(LongStr)
    ship_col = Required(bool, default=True)
    ship_courier = Optional(str)  # Default shipping courier and account #
    customer = Required(Customer)


class Supplier(Customer):
    purchase__orders = Set('Purchase_Order')


class Sale(db.Entity):
    id = PrimaryKey(int, auto=True)
    Number = Required(str, unique=True)  # Invoice number
    created_date_time = Optional(datetime, default=lambda: datetime.now())  # Time of Sale
    total = Required(Decimal)  # total value
    customer = Required(Customer)
    invoice_lines = Set('Invoice_line')
    posted = Required(bool)
    posted_date = Optional(datetime)  # Date and time that the invoice was posted.
    invoice_lines_shiped = Set('Invoice_line_shiped')
    shipments = Set('Shipment')
    user = Required('User')


class Purchase_Order(db.Entity):
    id = PrimaryKey(int, auto=True)
    number = Required(int)  # P.O. Number
    supplier = Required(Supplier)
    p_o_lines = Set('PO_line')
    po_lines_received = Set('Po_line_received')
    Autorized_by = Optional(str)
    last_edited = Optional(datetime, default=lambda: datetime.now())
    last_editor = Optional(str)
    user = Required('User')


class Invoice_line(db.Entity):
    id = PrimaryKey(int, auto=True)
    part = Required(Part)
    unit = Optional(int)  # number of units sold
    sale = Required(Sale)
    date_time = Optional(str)


class PO_line(db.Entity):
    id = PrimaryKey(int, auto=True)
    purchase__order = Required(Purchase_Order)
    part = Required(Part)
    unit = Required(int, default=1)  # Number of units being purchased
    date_time = Required(datetime, default=lambda: datetime.now())


class Shipment(db.Entity):
    id = PrimaryKey(int, auto=True)
    ship_method = Optional(str)
    ship_collect = Optional(bool)
    waybill = Optional(str)
    date = Optional(date)
    sales = Set(Sale)


class Po_line_received(PO_line):
    purchase__order = Required(Purchase_Order)


class Invoice_line_shiped(Invoice_line):
    sale = Required(Sale)


class WorkOrder(Sale):
    technician = Required(str)
    hours = Optional(str)
    job_type = Required(str)  # Repair, rebuilt for stock, mod exchange, or warranty


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    abreviation = Required(str, unique=True)
    purchase__orders = Set(Purchase_Order)
    authorized_sales = Required(bool)
    authorized_purchase = Optional(bool)
    authorized_manager = Optional(bool)
    sales = Set(Sale)


db.generate_mapping()
