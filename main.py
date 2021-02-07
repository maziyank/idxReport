from idxReport import idxReport

if __name__ == "__main__":
    idx = idxReport()
    print(idx.name, "is loaded\n")
    print(idx.getCompanyByCode('VIVA'))
    print(idx.downloadReport('VIVA', 'tw1', 2020))

