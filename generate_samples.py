"""Generate synthetic UAE court order PDFs for demo."""
from fpdf import FPDF
import os

OUT = "sample-data"
os.makedirs(OUT, exist_ok=True)


class Doc(FPDF):
    def __init__(self):
        super().__init__()
        self.set_margins(20, 20, 20)
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self._lh = 6  # default line height

    def gap(self, mm=5):
        self.ln(mm)

    def rule(self):
        self.ln(2)
        self.set_draw_color(150, 150, 150)
        x1 = self.l_margin
        x2 = self.w - self.r_margin
        self.line(x1, self.get_y(), x2, self.get_y())
        self.ln(3)

    def write_line(self, text, bold=False, size=11, align="L", lh=None):
        style = "B" if bold else ""
        self.set_font("Helvetica", style=style, size=size)
        line_h = lh or max(size * 0.45, 5)
        self.multi_cell(
            w=self.w - self.l_margin - self.r_margin,
            h=line_h,
            text=text,
            align=align,
            new_x="LMARGIN",
            new_y="NEXT",
        )


def sample3_dubai_freeze():
    d = Doc()
    d.write_line("DUBAI COURTS", bold=True, size=16, align="C")
    d.write_line("Judicial Department - Civil Execution Section", size=10, align="C")
    d.rule()
    d.write_line("Court Reference No.: DC/EX/2024/00341", bold=True)
    d.write_line("Date: 14 March 2024")
    d.gap()
    d.write_line("TO:  The Compliance and AML Department", bold=True)
    d.write_line("     Emirates NBD Bank - Dubai, UAE")
    d.gap()
    d.write_line("SUBJECT: ORDER TO FREEZE ACCOUNTS AND ASSETS", bold=True, size=12)
    d.rule()
    d.write_line(
        "Pursuant to Case No. 1872/2024 before the Dubai Court of First Instance, "
        "Execution Circuit, and in accordance with Federal Decree-Law No. 42 of 2022, "
        "you are hereby directed to immediately FREEZE all bank accounts, financial "
        "assets, investments, and safety deposit boxes held by the following individual:"
    )
    d.gap()
    d.write_line("Full Name    :  Tariq Hassan Al-Farouqi", bold=True)
    d.write_line("Emirates ID  :  784-1978-1234567-1", bold=True)
    d.write_line("Passport No. :  A9876543 (UAE)", bold=True)
    d.write_line("Date of Birth:  12 June 1978", bold=True)
    d.gap()
    d.write_line(
        "This order is effective immediately upon receipt. No withdrawals, transfers, "
        "or any transactions shall be permitted until a subsequent written order is "
        "issued by this Court."
    )
    d.gap()
    d.write_line(
        "The bank is required to confirm compliance within 24 hours to the "
        "Court Execution Department."
    )
    d.rule()
    d.write_line("Issued by: Judge Mohammed Al-Shamsi", size=10)
    d.write_line("Dubai Court of First Instance - Execution Circuit", size=10)
    d.output(f"{OUT}/sample3_dubai_freeze.pdf")
    print("  sample3_dubai_freeze.pdf")


def sample4_abudhabi_unfreeze():
    d = Doc()
    d.write_line("ABU DHABI JUDICIAL DEPARTMENT", bold=True, size=14, align="C")
    d.write_line("Department of Execution and Judicial Enforcement", size=10, align="C")
    d.write_line("Abu Dhabi - United Arab Emirates", size=10, align="C")
    d.gap()
    d.write_line("Ref: ADJD/EX/2024/00789          Date: 22 April 2024", size=10)
    d.rule()
    d.write_line("To Whom It May Concern:", bold=True)
    d.write_line("Central Bank of the UAE / All Licensed Banks Operating in the UAE")
    d.gap()
    d.write_line("Re: Lifting of Asset Freeze Order - Case No. 4421/2023", bold=True, size=12)
    d.gap()
    d.write_line(
        "We refer to our previous circular dated 5 November 2023 regarding the "
        "freezing of assets belonging to the below-named individual. "
        "The Abu Dhabi Judicial Department hereby notifies all concerned parties "
        "that the Court of Appeal has issued a ruling to LIFT and CANCEL the asset "
        "freeze order in its entirety. Banks are instructed to UNFREEZE all accounts "
        "and restore full access to the account holder with immediate effect."
    )
    d.gap()
    d.write_line("Account Holder Details:", bold=True)
    d.write_line("Name          :  Fatima Khalid Al-Mansouri")
    d.write_line("Emirates ID   :  784-1985-9876543-2")
    d.write_line("Trade License :  TL-ADJD-2019-44821")
    d.write_line("Nationality   :  Emirati")
    d.gap()
    d.write_line(
        "Please update your records accordingly and ensure all restrictions are "
        "removed within 48 hours. Confirmation must be submitted to this department."
    )
    d.rule()
    d.write_line("Judicial Officer: Dr. Aisha Al-Ketbi", size=10)
    d.write_line("Abu Dhabi Judicial Department - Execution Division", size=10)
    d.output(f"{OUT}/sample4_abudhabi_unfreeze.pdf")
    print("  sample4_abudhabi_unfreeze.pdf")


def sample5_sharjah_freeze():
    d = Doc()
    d.write_line("Sharjah Courts", bold=True, size=16, align="C")
    d.write_line("Ruler of Sharjah - Civil Execution Division", size=10, align="C")
    d.gap()
    d.write_line("Order Type : Asset Freeze Notification")
    d.write_line("Case No.   : SHJ/2024/CIV/0558")
    d.write_line("Issued On  : 3 February 2024")
    d.rule()
    d.write_line("To: Operations and Compliance - Central Bank UAE", bold=True)
    d.gap()
    d.write_line(
        "By the order of Sharjah Civil Court - Execution Department, all banking "
        "institutions are instructed to place an immediate FREEZE on all financial "
        "accounts, deposits, and assets registered under:"
    )
    d.gap()
    d.write_line("Name           : Robert James Whitfield", bold=True)
    d.write_line("Passport       : GBR-PX991234", bold=True)
    d.write_line("Emirates ID    : 784-1975-3456789-3", bold=True)
    d.write_line("Residence Visa : SHJ-VIS-2021-8812", bold=True)
    d.gap()
    d.write_line(
        "This freeze is in connection with civil litigation proceedings. No financial "
        "institution shall allow any debit, transfer, closure, or encumbrance on any "
        "account or asset until further written notice from Sharjah Courts."
    )
    d.rule()
    d.write_line("Court Registrar - Sharjah Court of First Instance", size=10)
    d.output(f"{OUT}/sample5_sharjah_freeze.pdf")
    print("  sample5_sharjah_freeze.pdf")


def sample6_ajman_unfreeze():
    d = Doc()
    d.write_line("AJMAN COURT", bold=True, size=13, align="C")
    d.write_line("Civil and Commercial Department", size=10, align="C")
    d.gap()
    d.write_line("Date: 9 May 2024")
    d.write_line("File Ref: AJM-2024-EX-0112")
    d.gap()
    d.write_line("To: The Compliance Manager", bold=True)
    d.write_line("    Any Bank Holding Assets of the Below-Named Party")
    d.gap()
    d.write_line(
        "Please be informed that Ajman Court has resolved Case No. AJM-2023-CIV-0778 "
        "and has issued an order to UNFREEZE and RELEASE all previously restricted "
        "accounts and assets belonging to:"
    )
    d.gap()
    d.write_line("Name        : Priya Suresh Nair")
    d.write_line("Nationality : Indian")
    d.write_line("Emirates ID : 784-1990-7654321-6")
    d.write_line("Passport    : M2345678")
    d.gap()
    d.write_line(
        "The bank is requested to reactivate all accounts and remove all holds "
        "effective immediately. Please notify this court once the process is complete."
    )
    d.gap()
    d.write_line("Court Clerk - Ajman Civil Court", size=10)
    d.output(f"{OUT}/sample6_ajman_unfreeze.pdf")
    print("  sample6_ajman_unfreeze.pdf")


print("Generating sample PDFs...")
sample3_dubai_freeze()
sample4_abudhabi_unfreeze()
sample5_sharjah_freeze()
sample6_ajman_unfreeze()
print(f"\nDone. Files saved to ./{OUT}/")
