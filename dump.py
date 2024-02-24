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
        try:
            if not is_first_iteration:
                print("Waiting for ", loop_dely_in_seconds, " seconds")
                time.sleep(loop_dely_in_seconds)
            else:
                is_first_iteration = False

            print("Dumping page: ", page)

            response = requests.get('https://www.edaalat.org/request/cases?q=&page='+ str(page))
            data = response.json()
        
        


            for case in data["cases"]:
                dump_to_file("Case #" + str(case_numer))

                case_id = case["data"]["ID"]
                dump_to_file("Case ID: ", case_id)

                case_title = case["data"]["TITLE"]
                dump_to_file("Case Title: ", case_title)

                try:
                    case_plaintiff = case_title.split(": ")[1][0:-11]
                    dump_to_file("Case Plaintiff: ", case_plaintiff)

                    case_accused = case_title.split(": ")[2][0:-12]
                    dump_to_file("Case Accused: ", case_accused)

                    case_court = case_title.split(": ")[3]
                    dump_to_file("Case Court: ", case_court)
                except Exception as e:
                    dump_to_file("parse error", e)



                case_subject = case["data"]["CASESUBJECT"]
                dump_to_file("Case Subject: ", case_subject)

                time.sleep(0.2)
                case_details = requests.get("https://www.edaalat.org/request/cases/" + str(case_id))
                case_details = case_details.json()
                dump_to_file("Case Details: ", case_details)

                # check if there is attachment in the case details and download the attachment
                num = 0

                if "CMS.HSTMINUTECASES" in case_details:
                    for data in case_details["CMS.HSTMINUTECASES"]:
                        if "CMS.HSTMINUTE" in data:
                            for minute in data["CMS.HSTMINUTE"]:
                                try:
                                    dump_to_file("Minute: ", minute["MINUTETEXT"])

                                    # download the minute and create new file and write the minute in it
                                    result = requests.get("https://www.edaalat.org/cases-files/" + minute["MINUTETEXT"])
                                    with open("data/attachments/report" + str(case_numer) + "_" + str(num) + ".html", "w") as file:
                                        file.write(result.text)
                                    num += 1
                                    time.sleep(0.2)
                                except Exception as e:
                                    print("no doc for download", e, case_numer)
                            
                if "CMS.LTRLETTERCASE" in case_details:
                    for document in case_details["CMS.LTRLETTERCASE"]:

                        if "CMS.LTRLETTER" in document:
                            for letter in document["CMS.LTRLETTER"]:
                                try:
                                    dump_to_file("Letter: ", letter["LETTERTEXT"])

                                    # download the letter and create new file and write the letter in it
                                    result = requests.get("https://www.edaalat.org/cases-files/" + letter["LETTERTEXT"])
                                    with open("data/attachments/letter" + str(case_numer) + "_" + str(num) + ".html", "w") as file:
                                        file.write(result.text)
                                    num += 1
                                    time.sleep(0.2)

                                except Exception as e:
                                    print("no doc for download", e, case_numer)




                        
                        if "CMS.LTRLETTERATTACHMENT" in document:
                            
                            for attachment in document["CMS.LTRLETTERATTACHMENT"]:
                                try:
                                    dump_to_file("Attachment: ", attachment["ATTACHEDDOCUMENT"])

                                    # download the pdf attachment and create new file and write the attachment in it

                                    result = requests.get("https://www.edaalat.org/cases-files/" + attachment["ATTACHEDDOCUMENT"])
                                    with open("data/attachments/attachment_" + str(case_numer) + "_" + str(num) +".pdf", "wb") as file:
                                        file.write(result.content)
                                    
                                    num += 1
                                    time.sleep(0.2)
                                except Exception as e:
                                    print("no doc for download", e, case_numer)



                


                dump_to_file("==================================SEPERATOR==================================")
                print("Case number: ", case_numer, " is dumped")
                print("==================================SEPERATOR==================================")


                case_numer += 1
                current_page = page
        except Exception as e:
            print("An error occured: ", e, case_numer, current_page)
            continue

def dump_to_file(text, *args):
    with open("data/data.txt", "a") as file:
        file.write(text)
        for arg in args:
            file.write(str(arg))
        file.write("\n")
    

def main():
    start_page = 1
    end_page = 20
    loop_dely_in_seconds = 3

    try:
        dump(start_page, end_page, loop_dely_in_seconds)
    except Exception as e:
        print("An error occured: ", e, case_numer, current_page)

    finally:
        print("Last case number: ",  case_numer)
        print("Last page number: ",  current_page)



if __name__ == "__main__":
    main()