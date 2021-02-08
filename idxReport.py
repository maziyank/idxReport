import requests
import json
import zipfile
import tempfile
import os

baseUrl = "https://www.idx.co.id/umbraco/Surface/"
customheaders = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

class idxReport:       
    def __init__(self):
        self.name = 'IDX Report'
        self.companies = self._fetchCompanies()   
        if not os.path.exists(os.path.join(tempfile.gettempdir(), 'idxReport')): 
            os.mkdir(os.path.join(tempfile.gettempdir(), 'idxReport'))      
    
    def _fetchCompanies(self):        
        response = requests.get(baseUrl + "Helper/GetEmiten?emitenType=s", headers=customheaders)
        companies =  dict()
        for company in response.json(): companies[company['KodeEmiten']] = company['NamaEmiten']
        return companies

    def getCompanies(self):
        return self.companies

    def getCompanyByCode(self, code):  
        return { 'code': code, 'name': self.companies[code] }     

    def getReport(self, code, period, year):        
        url = baseUrl + "ListedCompany/GetFinancialReport?year={}&reportType=rdf&periode={}&kodeEmiten={}".format(year, period, code)
        response = requests.get(url, headers=customheaders)
        if response.status_code == 200:
            data = response.json()
            if (data['ResultCount'] > 0):
                return list(filter(lambda x: x['File_Name'] == 'instance.zip', data['Results'][0]['Attachments']))[0]
            else:
                raise Exception("Not Found")    
        else:
            raise Exception("Can't fetch data")
    
    def _genFileName(self, code, period, year):
        return '_'.join([code, period, str(year)])

    def downloadReport(self, code, period, year, saveToDir = None):        
        saveDir = os.path.join(tempfile.gettempdir(), 'idxReport') if saveToDir == None else saveToDir
        url = self.getReport(code, period, year)['File_Path']
        r = requests.get(url, stream=True)
        filePath = os.path.join(saveDir, self._genFileName(code, period, year)) + '.zip'

        with open(filePath, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)

        with zipfile.ZipFile(filePath, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(saveDir, self._genFileName(code, period, year)))

        return saveDir
        

        