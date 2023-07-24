from faker import Faker
import random

class FakeData():
    def __init__(self) -> None:
        self.locations     = ['de_DE', 'de_AT', 'de_CH']
        self.country_codes = ['DE', 'AT', 'CH']
        self.currencies    = ['EUR', 'EUR', 'CHF']
        self.weights       = [0.5, 0.3, 0.2]
        
        banks_de = [
            "Deutsche Bank",
            "Commerzbank",
            "KfW Bank",
            "DZ Bank",
            "UniCredit Bank",
            "Sparkasse Köln",
            "Bayerische Landesbank",
            "Sparkasse München",
            "Sparkasse Berlin",
            "Landesbank Hessen-Thüringen"
        ]
        banks_at = [
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
        banks_ch = [
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
        
        self.banks = [banks_de, banks_at, banks_ch]
    
    def _get_bank_name(self, code): 
        i = self.country_codes.index(code)

        return random.choice(self.banks[i])
    
    def _get_currency(self, code):
        i = self.country_codes.index(code)
        return self.currencies[i]
    
    def _get_email(self, company_name, country_code):
        '''
            Generate a fake email address based on the company name
            Remove special characters and make the name lower case
        '''
        whitelist = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        company_name = ''.join(filter(whitelist.__contains__, company_name))
        company_name = company_name.lower()
        return 'www.' + company_name + '.' + country_code.lower()
    
    def _get_start_date(self):
        '''
            Start year between 2015 and 2023
            Always start on the first day of the month + never start in December
        '''
        years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
        months= ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11']
        
        yyyy = random.choice(years)
        mm = random.choice(months)
        dd = '01'

        return dd + '.' + mm + '.' + yyyy
    
    def _get_end_date(self, start_date):
        '''
            Always end on the last day of the same month (as the start date)
        '''
        if start_date[3:5] in ['01', '03', '05', '07', '08', '10']:
            return '31' + '.' + start_date[3:10]
        else:
            return '30' + '.' + start_date[3:10]
        
    def _get_due_date(self, start_date):
        '''
            Due date between the 20th and 30th of the next month (from start date)
        '''
        dates = ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
        months= ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        month_i = months.index(start_date[3:5])

        dd = random.choice(dates)
        mm = months[month_i+1]
        yyyy = start_date[6:10]

        return dd + '.' + mm + '.' + yyyy

    def __call__(self, num_invoices):
        # Every list element is a dictionary for a document
        fake_data = []
        for _ in range(num_invoices):
            fake_doc = dict()

            l = random.choices(self.locations, self.weights, k=1)
            
            fake = Faker(l[0])

            fake_doc['R_Name']       = fake.company()
            company = fake_doc['R_Name'].split()
            if company[-1] not in {'Inc', 'e.G.', 'LLC', 'GmbH', 'AG', 'KG', 'Ltd'}:
                fake_doc['R_Name'] += ' GmbH'
            fake_doc['R_Street']     = fake.street_name()
            fake_doc['R_HouseNumber']= fake.building_number()
            if random.random() < 0.6:
                fake_doc['R_HouseNumber'] += random.choice(['a', 'b', 'c'])
            fake_doc['R_ZIP']        = fake.postcode()
            fake_doc['R_City']       = fake.city()
            fake_doc['R_Country']    = fake.current_country()
            fake_doc['R_VAT']        = fake.current_country_code() + str(fake.random_number(digits=9, fix_len=True))
            fake_doc['S_Name']       = fake.company()
            company = fake_doc['S_Name'].split()
            if company[-1] not in {'Inc', 'e.G.', 'LLC', 'GmbH', 'AG', 'KG', 'Ltd'}:
                fake_doc['S_Name'] += ' GmbH'
            fake_doc['S_Street']     = fake.street_name()
            fake_doc['S_HouseNumber']= fake.building_number()
            if random.random() < 0.4:
                fake_doc['S_HouseNumber'] += random.choice(['a', 'b', 'c'])
            fake_doc['S_ZIP']        = fake.postcode()
            fake_doc['S_City']       = fake.city()
            fake_doc['S_Country']    = fake.current_country()
            fake_doc['S_VAT']        = fake.current_country_code() + str(fake.random_number(digits=9, fix_len=True))
            fake_doc['S_Bank']       = self._get_bank_name(fake.current_country_code())
            fake_doc['S_BIC']        = fake.swift8()
            fake_doc['S_IBAN']       = fake.iban()
            fake_doc['S_Tel']        = fake.phone_number()
            fake_doc['S_Email']      = fake.email()
            fake_doc['I_Number']     = str(fake.random_number(digits=9, fix_len=True))
            fake_doc['I_Amount']     = str(fake.random_number()) + ',' + str(fake.random_number(digits=2, fix_len=True))
            fake_doc['I_Currency']   = self._get_currency(fake.current_country_code())
            fake_doc['Fax']          = fake.phone_number()
            fake_doc['Website']      = self._get_email(fake_doc['S_Name'], fake.current_country_code())
            fake_doc['Contact_Name'] = fake.name()
            fake_doc['Start_Date']   = self._get_start_date()
            fake_doc['End_Date']     = self._get_end_date(fake_doc['Start_Date'])
            fake_doc['I_Date']       = fake_doc['End_Date']
            fake_doc['I_DueDate']    = self._get_due_date(fake_doc['Start_Date'])

            fake_data.append(fake_doc)
        
        return fake_data