import os
import random
import json
from pathlib import Path
from typing import List, Tuple
from datetime import datetime, timedelta, timezone
from faker import Faker
from pydantic import BaseModel, Field, EmailStr, TypeAdapter

fake = Faker()

# ==============================================================================
# 1. BILLING SCHEMAS
# ==============================================================================

class PaymentMethod(BaseModel):
    payment_method_id: str = Field(..., pattern=r"^PM-[0-9]{6}$")
    type: str = Field(..., example="CREDIT_CARD")
    last_four: str = Field(..., pattern=r"^[0-9]{4}$")
    is_default: bool

class InvoiceItem(BaseModel):
    description: str
    amount: float

class Invoice(BaseModel):
    invoice_id: str = Field(..., pattern=r"^INV-[0-9]{8}$")
    customer_id: str  # Foreign Key linking to CRM record
    billing_account_id: str  # Foreign Key linking to Billing Account
    issue_date: str
    due_date: str
    total_amount: float
    status: str = Field(..., example="PAID")
    line_items: List[InvoiceItem]

class BillingAccount(BaseModel):
    billing_account_id: str = Field(..., pattern=r"^BILL-[0-9]{6}$")
    customer_id: str  # Foreign Key reference to CRM customer_id
    currency: str = "USD"
    current_balance: float
    autopay_enabled: bool
    payment_methods: List[PaymentMethod]
    invoices: List[Invoice]

# ==============================================================================
# 2. CRM SCHEMAS
# ==============================================================================

class ContactInfo(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    company: str

class CRMRecord(BaseModel):
    customer_id: str = Field(..., pattern=r"^CUST-[0-9]{6}$")
    billing_account_id: str  # Foreign Key reference to Billing entity
    contact: ContactInfo
    account_status: str
    lifetime_value: float
    created_at: str  # ISO timestamp between now and last 12 months

# ==============================================================================
# 3. SYNTHETIC GENERATORS
# ==============================================================================

def generate_billing_history_last_6_months(
    customer_id: str, 
    billing_account_id: str, 
    customer_created_at: datetime
) -> List[Invoice]:
    invoices = []
    now = datetime.now(timezone.utc)
    
    # Generate 6 monthly invoices going back 6 months (~30 days apart)
    for month_offset in range(6, 0, -1):
        issue_date = now - timedelta(days=30 * month_offset)
        
        # Ensure invoice issue date does not precede customer creation date
        if issue_date < customer_created_at:
            issue_date = customer_created_at + timedelta(days=1)
            
        due_date = issue_date + timedelta(days=15)
        
        plan_fee = round(random.uniform(40.0, 120.0), 2)
        taxes = round(plan_fee * 0.10, 2)
        total = round(plan_fee + taxes, 2)

        invoices.append(
            Invoice(
                invoice_id=f"INV-{fake.random_number(digits=8, fix_len=True)}",
                customer_id=customer_id,
                billing_account_id=billing_account_id,
                issue_date=issue_date.isoformat(),
                due_date=due_date.isoformat(),
                total_amount=total,
                status=random.choice(["PAID", "PAID", "PAID", "OVERDUE"]),
                line_items=[
                    InvoiceItem(description="Monthly Rate Plan", amount=plan_fee),
                    InvoiceItem(description="Regulatory Taxes & Fees", amount=taxes)
                ]
            )
        )
    return invoices

def generate_pair_crm_and_billing() -> Tuple[CRMRecord, BillingAccount]:
    customer_id = f"CUST-{fake.random_number(digits=6, fix_len=True)}"
    billing_account_id = f"BILL-{fake.random_number(digits=6, fix_len=True)}"

    # Generate customer creation date within the last 12 months (365 days)
    now = datetime.now(timezone.utc)
    random_days_ago = random.randint(1, 365)
    customer_created_at = now - timedelta(days=random_days_ago)

    # Generate 6 months of invoice history
    invoices = generate_billing_history_last_6_months(
        customer_id, billing_account_id, customer_created_at
    )
    
    calculated_ltv = round(sum(inv.total_amount for inv in invoices), 2)

    billing_account = BillingAccount(
        billing_account_id=billing_account_id,
        customer_id=customer_id,
        currency="USD",
        current_balance=0.0 if invoices[-1].status == "PAID" else invoices[-1].total_amount,
        autopay_enabled=fake.boolean(chance_of_getting_true=75),
        payment_methods=[
            PaymentMethod(
                payment_method_id=f"PM-{fake.random_number(digits=6, fix_len=True)}",
                type=random.choice(["CREDIT_CARD", "DEBIT_CARD", "ACH"]),
                last_four=str(fake.random_number(digits=4, fix_len=True)),
                is_default=True
            )
        ],
        invoices=invoices
    )

    crm_record = CRMRecord(
        customer_id=customer_id,
        billing_account_id=billing_account_id,
        contact=ContactInfo(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone=fake.phone_number(),
            company=fake.company()
        ),
        account_status=random.choice(["Active", "Delinquent", "Prospect"]),
        lifetime_value=calculated_ltv,
        created_at=customer_created_at.isoformat()
    )

    return crm_record, billing_account

def generate_datasets(count: int):
    crm_list: List[CRMRecord] = []
    billing_list: List[BillingAccount] = []

    for _ in range(count):
        crm_item, billing_item = generate_pair_crm_and_billing()
        crm_list.append(crm_item)
        billing_list.append(billing_item)

    crm_adapter = TypeAdapter(List[CRMRecord])
    billing_adapter = TypeAdapter(List[BillingAccount])

    crm_json = crm_adapter.dump_json(crm_list, indent=2).decode("utf-8")
    billing_json = billing_adapter.dump_json(billing_list, indent=2).decode("utf-8")

    return crm_json, billing_json

# ==============================================================================
# 4. EXECUTION & OUTPUT TO ../data DIRECTORY
# ==============================================================================

# Ensure directory ../data exists relative to execution location
output_dir = Path("../data")
output_dir.mkdir(parents=True, exist_ok=True)

crm_data, billing_data = generate_datasets(10)

crm_file_path = output_dir / "crm_records.json"
billing_file_path = output_dir / "billing_records.json"

with open(crm_file_path, "w") as f_crm:
    f_crm.write(crm_data)

with open(billing_file_path, "w") as f_billing:
    f_billing.write(billing_data)

print(f"Successfully generated datasets under '{output_dir.resolve()}':")
print(f" - {crm_file_path}")
print(f" - {billing_file_path}")