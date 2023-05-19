from faker import Faker
import random

class FakeData():
    def __init__(self, num = 1, det = True) -> None:
        self.locations = ['de_DE', 'de_AT', 'de_CH', 'en_GB', 'en_US', 'fr_FR', 'es_ES', 'pt_PT', 'it_IT', 'pl_PL']
        self.country_codes = ['DE', 'AT', 'CH', 'GB', 'US', 'FR', 'ES', 'PT', 'IT', 'PL']
        self.currencies = ['EUR', 'EUR', 'CHF', 'GBP', 'USD', 'EUR', 'EUR', 'EUR', 'EUR', 'PLN']
        self.weights = [0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05]
        self.NUM_INVOICES = num
        self.banks_de = [
    "Deutsche Bank",
    "Commerzbank",
    "KfW Bank",
    "DZ Bank",
    "UniCredit Bank",
    "Landesbank Baden-Württemberg",
    "Bayerische Landesbank",
    "HypoVereinsbank",
    "Norddeutsche Landesbank",
    "Landesbank Hessen-Thüringen"
]
        self.banks_at = [
    "Erste Group Bank",
    "Raiffeisen Bank International",
    "Bank Austria",
    "Bawag Group",
    "UniCredit Bank Austria",
    "Oberbank",
    "Volksbanken-Verbund",
    "HYPO NOE Landesbank",
    "Steiermärkische Bank und Sparkassen",
    "Oesterreichische Kontrollbank"
    ]
        self.banks_ch = [
    "UBS",
    "Credit Suisse",
    "Julius Baer Group",
    "Zurich Cantonal Bank",
    "Raiffeisen Switzerland",
    "PostFinance",
    "Swissquote",
    "LGT Bank",
    "Vontobel",
    "Banque Cantonale Vaudoise"
]
        self.banks_gb = [
    "HSBC",
    "Lloyds Banking Group",
    "Barclays",
    "NatWest Group",
    "Standard Chartered",
    "Santander UK",
    "Royal Bank of Scotland",
    "Co-operative Bank",
    "Virgin Money",
    "Metro Bank"
]
        self.banks_us = [
   "JPMorgan Chase",
    "Bank of America",
    "Wells Fargo",
    "Citigroup",
    "Goldman Sachs",
    "Morgan Stanley",
    "U.S. Bancorp",
    "PNC Financial Services",
    "Capital One Financial",
    "TD Bank" 
]
        self.banks_fr = [
    "BNP Paribas",
    "Crédit Agricole",
    "Société Générale",
    "Groupe BPCE",
    "Crédit Mutuel",
    "La Banque Postale",
    "Caisse d'Épargne",
    "Natixis",
    "HSBC France",
    "Banque Populaire"
]
        self.banks_es = [
    "Banco Santander",
    "BBVA",
    "CaixaBank",
    "Banco Sabadell",
    "Bankia",
    "Banco Popular",
    "Bankinter",
    "Kutxabank",
    "Unicaja Banco",
    "Ibercaja"
]
        self.banks_pt = [
    "Caixa Geral de Depósitos",
    "Novo Banco",
    "Banco Comercial Português",
    "Banco Santander Totta",
    "Banco BPI",
    "Crédito Agrícola",
    "Montepio Geral",
    "Banco Português de Investimento",
    "Bankinter",
    "EuroBic"
]
        self.banks_it = [
    "UniCredit",
    "Intesa Sanpaolo",
    "Banca Monte dei Paschi di Siena",
    "Banco BPM",
    "UBI Banca",
    "BPER Banca",
    "Credito Emiliano",
    "Cassa Depositi e Prestiti",
    "Banca Popolare di Sondrio",
    "Veneto Banca"
]
        self.banks_pl = [
    "PKO Bank Polski",
    "Bank Pekao",
    "mBank",
    "ING Bank Śląski",
    "Santander Bank Polska",
    "Bank Millennium",
    "BGŻ BNP Paribas",
    "Getin Noble Bank",
    "Alior Bank",
    "Idea Bank"
]
        self.det = det
        if self.det is True:
            random.seed(4320)
        self.locs = self.generate_locations()

    def generate_locations(self):
        locs = random.choices(self.locations, weights=self.weights, k=self.NUM_INVOICES)
        locs.sort()

        return locs
    
    def get_bank_name(self, code):
        banks = [self.banks_de, self.banks_at, self.banks_ch,
                 self.banks_gb, self.banks_us, self.banks_fr,
                 self.banks_es, self.banks_pt, self.banks_it, self.banks_pl]
        i = self.country_codes.index(code)

        return random.choice(banks[i])
    
    def get_currency(self, code):
        i = self.country_codes.index(code)
        return self.currencies[i]
    
    def get_email(self, company_name, country_code):
        whitelist = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        company_name = ''.join(filter(whitelist.__contains__, company_name))
        company_name = company_name.lower()
        return 'www.' + company_name + '.' + country_code.lower()
    
    def get_start_date(self):
        years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
        months= ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11']

        yyyy = random.choice(years)
        mm = random.choice(months)
        dd = '01'

        return dd + '.' + mm + '.' + yyyy
    
    def get_end_date(self, start_date):
        if start_date[3:5] in ['01', '03', '05', '07', '08', '10']:
            return '31' + '.' + start_date[3:10]
        else:
            return '30' + '.' + start_date[3:10]
        
    def get_due_date(self, start_date):
        dates = ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
        months= ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11']
        month_i = months.index(start_date[3:5])

        dd = random.choice(dates)
        mm = months[month_i+1]
        yyyy = start_date[6:10]

        return dd + '.' + mm + '.' + yyyy

class Agder_Energi(FakeData):
    def __init__(self, num=1, det=True) -> None:
        super().__init__(num, det)

    def get_fake_data(self):
        # Every list element is a dictionary for a document
        fake_data = []
        for l in self.locs:
            fake_doc = dict()
            fake = Faker(l)

            fake_doc['R_Name']      = fake.company() 
            fake_doc['R_Street']    = fake.street_name()
            fake_doc['R_HouseNumber']   = fake.building_number()
            fake_doc['R_ZIP']       = fake.postcode()
            fake_doc['R_City']      = fake.city()
            fake_doc['R_Country']   = fake.current_country()
            fake_doc['R_VAT']       = fake.current_country_code() + str(fake.random_number(digits=9, fix_len=True))
            fake_doc['S_Name']      = fake.company()
            fake_doc['S_Street']    = fake.street_name()
            fake_doc['S_HouseNumber']   = fake.building_number()
            fake_doc['S_ZIP']       = fake.postcode()
            fake_doc['S_City']      = fake.city()
            fake_doc['S_Country']   = fake.current_country()
            fake_doc['S_VAT']       = fake.current_country_code() + str(fake.random_number(digits=9, fix_len=True))
            fake_doc['S_Bank']      = self.get_bank_name(fake.current_country_code())
            fake_doc['S_BIC']       = fake.swift8()
            fake_doc['S_IBAN']      = fake.iban()
            fake_doc['S_Tel']       = fake.phone_number()
            fake_doc['S_Email']     = fake.email()
            fake_doc['I_Number']    = str(fake.random_number(digits=9, fix_len=True))
            fake_doc['I_Amount']    = str(fake.random_number()) + ',' + str(fake.random_number(digits=2, fix_len=True))
            fake_doc['I_Currency']  = self.get_currency(fake.current_country_code())
            fake_doc['Fax']         = fake.phone_number()
            fake_doc['Website']     = self.get_email(fake_doc['S_Name'], fake.current_country_code())
            fake_doc['Contact_name']= fake.name()
            fake_doc['Start_date']  = self.get_start_date()
            fake_doc['End_date']    = self.get_end_date(fake_doc['Start_date'])
            fake_doc['I_Date']      = fake_doc['End_date']
            fake_doc['I_DueDate']   = self.get_due_date(fake_doc['Start_date'])

            fake_data.append(fake_doc)
        
        return fake_data