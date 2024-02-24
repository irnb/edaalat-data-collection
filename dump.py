import requests
import json
import time

case_numer = 1
current_page = 1

def dump(start_page, end_page, loop_dely_in_seconds,):
    global case_numer
    global current_page
    is_first_iteration = True


    for page in range(start_page, end_page + 1):
        if not is_first_iteration:
            print("Waiting for ", loop_dely_in_seconds, " seconds")
            time.sleep(loop_dely_in_seconds)
        else:
            is_first_iteration = False

        print("Dumping page: ", page)

        response = requests.get('https://www.edaalat.org/request/cases?q=&page='+ str(page))
        data = response.json()
    
    


        for case in data["cases"]:
            print("Case #" + str(case_numer))

            case_id = case["data"]["ID"]
            print("Case ID: ", case_id)

            case_title = case["data"]["TITLE"]
            print("Case Title: ", case_title)

            try:
                case_plaintiff = case_title.split(": ")[1][0:-11]
                print("Case Plaintiff: ", case_plaintiff)

                case_accused = case_title.split(": ")[2][0:-12]
                print("Case Accused: ", case_accused)

                case_court = case_title.split(": ")[3]
                print("Case Court: ", case_court)
            except Exception as e:
                print("parse error", e)



            case_subject = case["data"]["CASESUBJECT"]
            print("Case Subject: ", case_subject)

            case_details = requests.get("https://www.edaalat.org/request/cases/" + str(case_id))
            case_details = case_details.json()
            print("Case Details: ", case_details)

            # check if there is attachment in the case details and download the attachment
            num = 0

            if "CMS.HSTMINUTECASES" in case_details:
                for data in case_details["CMS.HSTMINUTECASES"]:
                    if "CMS.HSTMINUTE" in data:
                        for minute in data["CMS.HSTMINUTE"]:
                            try:
                                print("Minute: ", minute["MINUTETEXT"])

                                # download the minute and create new file and write the minute in it
                                result = requests.get("https://www.edaalat.org/cases-files/" + minute["MINUTETEXT"])
                                with open("data/attachments/report" + str(case_numer) + "_" + str(num) + ".html", "w") as file:
                                    file.write(result.text)
                                num += 1
                            except Exception as e:
                                print("no doc for download", e)
                        
            if "CMS.LTRLETTERCASE" in case_details:
                for document in case_details["CMS.LTRLETTERCASE"]:

                    if "CMS.LTRLETTER" in document:
                        for letter in document["CMS.LTRLETTER"]:
                            try:
                                print("Letter: ", letter["LETTERTEXT"])

                                # download the letter and create new file and write the letter in it
                                result = requests.get("https://www.edaalat.org/cases-files/" + letter["LETTERTEXT"])
                                with open("data/attachments/letter" + str(case_numer) + "_" + str(num) + ".html", "w") as file:
                                    file.write(result.text)
                                num += 1
                            except Exception as e:
                                print("no doc for download", e)




                    
                    if "CMS.LTRLETTERATTACHMENT" in document:
                        
                        for attachment in document["CMS.LTRLETTERATTACHMENT"]:
                            try:
                                print("Attachment: ", attachment["ATTACHEDDOCUMENT"])

                                # download the pdf attachment and create new file and write the attachment in it

                                result = requests.get("https://www.edaalat.org/cases-files/" + attachment["ATTACHEDDOCUMENT"])
                                with open("data/attachments/attachment_" + str(case_numer) + "_" + str(num) +".pdf", "wb") as file:
                                    file.write(result.content)
                                
                                num += 1
                            except Exception as e:
                                print("no doc for download", e)



            


            print("==================================SEPERATOR==================================")
            
            case_numer += 1
            current_page = page

def main():
    start_page = 1
    end_page = 20
    loop_dely_in_seconds = 3

    try:
        dump(start_page, end_page, loop_dely_in_seconds)
    except Exception as e:
        print("An error occured: ", e)

    finally:
        print("Last case number: ",  case_numer)
        print("Last page number: ",  current_page)



if __name__ == "__main__":
    main()