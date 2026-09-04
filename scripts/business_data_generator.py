import os
import random
import json
from pathlib import Path
from typing import List, Tuple, Optional
from datetime import datetime, timedelta, timezone
from faker import Faker
from pydantic import BaseModel, Field, EmailStr, TypeAdapter

fake = Faker()

# ==============================================================================
# 1. BILLING SCHEMAS
# ==============================================================================

class PaymentMethod(BaseModel):
    payment_method_id: str = Field(..., pattern=r"^PM-[0-9]{6}$")
    type: str = Field(..., json_schema_extra={"example": "CREDIT_CARD"})
    last_four: str = Field(..., pattern=r"^[0-9]{4}$")
    is_default: bool

class InvoiceItem(BaseModel):
    description: str
    amount: float

class Invoice(BaseModel):
    invoice_id: str = Field(..., pattern=r"^INV-[0-9]{8}$")
    customer_id: str  # Foreign Key linking to CRM record
    billing_account_id: str  # Foreign Key linking to Billing Account
    plan_id: str  # Foreign Key linking to Product Catalog plan
    issue_date: str
    due_date: str
    total_amount: float
    status: str = Field(..., json_schema_extra={"example": "PAID"})
    line_items: List[InvoiceItem]

class BillingAccount(BaseModel):
    billing_account_id: str = Field(..., pattern=r"^BILL-[0-9]{6}$")
    customer_id: str  # Foreign Key reference to CRM customer_id
    device_id: str  # Foreign Key reference to Product Catalog device
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
    current_plan_id: str  # Foreign Key reference to Product Catalog plan
    eligible_promotion_ids: List[str]  # Foreign Keys reference to Promotions
    contact: ContactInfo
    account_status: str
    lifetime_value: float
    created_at: str  # ISO timestamp between now and last 12 months

# ==============================================================================
# 2b. PRODUCT CATALOG & PROMOTIONS SCHEMAS
# ==============================================================================

class Plan(BaseModel):
    plan_id: str = Field(..., pattern=r"^PLAN-[0-9]{3}$")
    name: str
    data_allowance_gb: int
    talk_minutes: int
    text_messages: int
    monthly_price: float
    hotspot_included: bool
    international_calling: bool

class Device(BaseModel):
    device_id: str = Field(..., pattern=r"^DEV-[0-9]{4}$")
    brand: str
    model: str
    storage_gb: int
    color: str
    retail_price: float
    release_year: int

class ProductCatalog(BaseModel):
    plans: List[Plan]
    devices: List[Device]

class Promotion(BaseModel):
    promotion_id: str = Field(..., pattern=r"^PROMO-[0-9]{4}$")
    title: str
    description: str
    promo_type: str = Field(..., json_schema_extra={"example": "PLAN_OFFER"})  # PLAN_OFFER | DEVICE_PROMO | BUNDLE
    target_plan_id: Optional[str] = None
    target_device_id: Optional[str] = None
    discount_amount: float
    eligible_account_statuses: List[str]
    valid_until: str

# ==============================================================================
# 2c. CURATED CATALOG & PROMOTIONS
# ==============================================================================

DEFAULT_PLANS = [
    Plan(plan_id="PLAN-001", name="Essential", data_allowance_gb=5, talk_minutes=500,
         text_messages=500, monthly_price=40.0, hotspot_included=False, international_calling=False),
    Plan(plan_id="PLAN-002", name="Standard", data_allowance_gb=20, talk_minutes=1000,
         text_messages=1000, monthly_price=60.0, hotspot_included=True, international_calling=False),
    Plan(plan_id="PLAN-003", name="Premium", data_allowance_gb=50, talk_minutes=0,
         text_messages=0, monthly_price=80.0, hotspot_included=True, international_calling=True),
    Plan(plan_id="PLAN-004", name="Family", data_allowance_gb=100, talk_minutes=0,
         text_messages=0, monthly_price=120.0, hotspot_included=True, international_calling=True),
    Plan(plan_id="PLAN-005", name="Unlimited", data_allowance_gb=0, talk_minutes=0,
         text_messages=0, monthly_price=90.0, hotspot_included=True, international_calling=True),
]

DEFAULT_DEVICES = [
    Device(device_id="DEV-1001", brand="Apple", model="iPhone 15", storage_gb=128,
           color="Black", retail_price=799.0, release_year=2023),
    Device(device_id="DEV-1002", brand="Apple", model="iPhone 15 Pro", storage_gb=256,
           color="Natural Titanium", retail_price=1099.0, release_year=2023),
    Device(device_id="DEV-1003", brand="Samsung", model="Galaxy S24", storage_gb=128,
           color="Onyx Black", retail_price=799.0, release_year=2024),
    Device(device_id="DEV-1004", brand="Samsung", model="Galaxy S24 Ultra", storage_gb=512,
           color="Titanium Gray", retail_price=1199.0, release_year=2024),
    Device(device_id="DEV-1005", brand="Google", model="Pixel 8", storage_gb=128,
           color="Obsidian", retail_price=699.0, release_year=2023),
]

DEFAULT_CATALOG = ProductCatalog(plans=DEFAULT_PLANS, devices=DEFAULT_DEVICES)


def build_promotions() -> List[Promotion]:
    """Curated offers referencing catalog plans/devices."""
    now = datetime.now(timezone.utc)
    valid_until = (now + timedelta(days=90)).isoformat()
    return [
        Promotion(
            promotion_id="PROMO-0001", title="Premium Upgrade Discount",
            description="$10/mo off the Premium plan for the first 12 months.",
            promo_type="PLAN_OFFER", target_plan_id="PLAN-003", discount_amount=10.0,
            eligible_account_statuses=["Active", "Prospect"], valid_until=valid_until,
        ),
        Promotion(
            promotion_id="PROMO-0002", title="Family Bundle Deal",
            description="$15/mo off the Family plan with 2+ lines.",
            promo_type="PLAN_OFFER", target_plan_id="PLAN-004", discount_amount=15.0,
            eligible_account_statuses=["Active"], valid_until=valid_until,
        ),
        Promotion(
            promotion_id="PROMO-0003", title="New Device Trade-In Bonus",
            description="$200 off any flagship device with a qualifying trade-in.",
            promo_type="DEVICE_PROMO", target_device_id=None, discount_amount=200.0,
            eligible_account_statuses=["Active", "Prospect"], valid_until=valid_until,
        ),
        Promotion(
            promotion_id="PROMO-0004", title="Premium + Pixel Bundle",
            description="Premium plan bundled with a Pixel 8 at $150 off.",
            promo_type="BUNDLE", target_plan_id="PLAN-003", target_device_id="DEV-1005",
            discount_amount=150.0, eligible_account_statuses=["Active"], valid_until=valid_until,
        ),
        Promotion(
            promotion_id="PROMO-0005", title="Win-Back Unlimited Offer",
            description="Unlimited plan at $75/mo to win back delinquent accounts.",
            promo_type="PLAN_OFFER", target_plan_id="PLAN-005", discount_amount=15.0,
            eligible_account_statuses=["Delinquent"], valid_until=valid_until,
        ),
    ]


DEFAULT_PROMOTIONS = build_promotions()

# ==============================================================================
# 3. SYNTHETIC GENERATORS
# ==============================================================================

def generate_billing_history_last_6_months(
    customer_id: str,
    billing_account_id: str,
    customer_created_at: datetime,
    plan: Plan
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

        plan_fee = plan.monthly_price
        taxes = round(plan_fee * 0.10, 2)
        total = round(plan_fee + taxes, 2)

        invoices.append(
            Invoice(
                invoice_id=f"INV-{fake.random_number(digits=8, fix_len=True)}",
                customer_id=customer_id,
                billing_account_id=billing_account_id,
                plan_id=plan.plan_id,
                issue_date=issue_date.isoformat(),
                due_date=due_date.isoformat(),
                total_amount=total,
                status=random.choice(["PAID", "PAID", "PAID", "OVERDUE"]),
                line_items=[
                    InvoiceItem(description=f"{plan.name} — Monthly Rate Plan", amount=plan_fee),
                    InvoiceItem(description="Regulatory Taxes & Fees", amount=taxes)
                ]
            )
        )
    return invoices


def generate_pair_crm_and_billing() -> Tuple[CRMRecord, BillingAccount]:
    customer_id = f"CUST-{fake.random_number(digits=6, fix_len=True)}"
    billing_account_id = f"BILL-{fake.random_number(digits=6, fix_len=True)}"

    plan = random.choice(DEFAULT_CATALOG.plans)
    device = random.choice(DEFAULT_CATALOG.devices)

    # Generate customer creation date within the last 12 months (365 days)
    now = datetime.now(timezone.utc)
    random_days_ago = random.randint(1, 365)
    customer_created_at = now - timedelta(days=random_days_ago)

    # Generate 6 months of invoice history for the assigned plan
    invoices = generate_billing_history_last_6_months(
        customer_id, billing_account_id, customer_created_at, plan
    )

    calculated_ltv = round(sum(inv.total_amount for inv in invoices), 2)
    account_status = random.choice(["Active", "Delinquent", "Prospect"])

    eligible_promotion_ids = [
        promo.promotion_id
        for promo in DEFAULT_PROMOTIONS
        if account_status in promo.eligible_account_statuses
    ][:2]  # cap at 2 offers per customer for realism

    billing_account = BillingAccount(
        billing_account_id=billing_account_id,
        customer_id=customer_id,
        device_id=device.device_id,
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
        current_plan_id=plan.plan_id,
        eligible_promotion_ids=eligible_promotion_ids,
        contact=ContactInfo(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone=fake.phone_number(),
            company=fake.company()
        ),
        account_status=account_status,
        lifetime_value=calculated_ltv,
        created_at=customer_created_at.isoformat()
    )

    return crm_record, billing_account


def generate_datasets(count: int) -> Tuple[str, str, str, str]:
    """Returns (catalog_json, promotions_json, crm_json, billing_json)."""
    crm_list: List[CRMRecord] = []
    billing_list: List[BillingAccount] = []

    for _ in range(count):
        crm_item, billing_item = generate_pair_crm_and_billing()
        crm_list.append(crm_item)
        billing_list.append(billing_item)

    catalog_json = TypeAdapter(ProductCatalog).dump_json(
        DEFAULT_CATALOG, indent=2
    ).decode("utf-8")
    promotions_json = TypeAdapter(List[Promotion]).dump_json(
        DEFAULT_PROMOTIONS, indent=2
    ).decode("utf-8")
    crm_json = TypeAdapter(List[CRMRecord]).dump_json(
        crm_list, indent=2
    ).decode("utf-8")
    billing_json = TypeAdapter(List[BillingAccount]).dump_json(
        billing_list, indent=2
    ).decode("utf-8")

    return catalog_json, promotions_json, crm_json, billing_json

# ==============================================================================
# 4. EXECUTION & OUTPUT TO ../data DIRECTORY
# ==============================================================================

# Ensure output goes to <project root>/data/business_data regardless of working directory
output_dir = Path(__file__).resolve().parent.parent / "data" / "business_data"
output_dir.mkdir(parents=True, exist_ok=True)

catalog_data, promotions_data, crm_data, billing_data = generate_datasets(10)

catalog_file_path = output_dir / "product_catalog.json"
promotions_file_path = output_dir / "promotions.json"
crm_file_path = output_dir / "crm_records.json"
billing_file_path = output_dir / "billing_records.json"

with open(catalog_file_path, "w") as f_catalog:
    f_catalog.write(catalog_data)

with open(promotions_file_path, "w") as f_promotions:
    f_promotions.write(promotions_data)

with open(crm_file_path, "w") as f_crm:
    f_crm.write(crm_data)

with open(billing_file_path, "w") as f_billing:
    f_billing.write(billing_data)

print(f"Successfully generated datasets under '{output_dir.resolve()}':")
print(f" - {catalog_file_path}")
print(f" - {promotions_file_path}")
print(f" - {crm_file_path}")
print(f" - {billing_file_path}")