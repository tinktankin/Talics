from django.shortcuts import render
from django.http import HttpResponse
from .models import Staging, GoodRecords, BadRecords
from django_pandas.io import read_frame
import re
from datetime import date
from user.models import User
from mandates.models import Mandates
from system.models import CandidateStatus
from .models import Client

def index2(request):

    df = read_frame(Staging.objects.all())
    # good = read_frame(GoodRecords.objects.all())
    # bad = read_frame(BadRecords.objects.all())
    df = df.astype(str)
    token = []


    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    for index, row in df.iterrows():
        dict = {}

        # reqt_date = datetime.strptime(row['reqt_date'], "%Y-%m-%d").date()
        # print(reqt_date)
        # if datetime.strptime(row['date_cv_submitted'], "%Y-%m-%d").date() < reqt_date:
        #     dict['date_cv_submitted'] = 'Should be after reqt date'
        #     row['reason'] = dict

        if row['recruiter'] not in User.objects.values_list('FullName', flat = True):
            dict['recruiter'] = 'Not in the List'

        if row['client'] not in Client.objects.values_list('ClientName', flat = True):
            dict['client'] = 'Not in the List'

        if row['vacancy_code'] not in Mandates.objects.values_list('VacancyCode', flat = True):
            dict['vacancy_code'] = 'Not in the List'

        if row['reqt_date'] not in Mandates.objects.values_list('AssignedDate', flat = True):
            dict['reqt_date'] = 'Not in the List'

        if row['date_cv_submitted'] < row['reqt_date']:
            dict['date_cv_submitted'] = 'Should be after reqt date'


        if 'client' not in dict.keys() or 'vacancy_code' not in dict.keys():
            pass
        else:
            k = row['client'] + row['vacancy_code']
            if k in token:
                dict['candidate_name'] = 'Not unique'
            else:
                token.append(k)



        if CandidateStatus.objects.filter(StageID = row['current_status']).exists():
            stagedb = CandidateStatus.objects.filter(StageID = row['current_status']).values_list('StageName', flat = True)
            if row['current_status_desc'] not in stagedb:
                dict['current_status_desc'] = 'Mismatch!'

        else:
            dict['current_status'] = 'Not in the List'



        if len(row['contact_details_mobile']) != 10:
            dict['contact_details_mobile'] = 'Not 10 digits'

        ph = []
        if len(row['contact_details_phone2']) != 10:
            ph.append('Not 10 digits')
            dict['contact_details_phone2'] = ph


        if row['contact_details_phone2'] == row['contact_details_mobile']:
            if dict['contact_details_phone2']:
                ph.append('Repeated Contact')
                dict['contact_details_phone2'] = ph


        if not row['total_exp'].replace('.', '', 1).isdigit():
            dict['total_exp'] = 'Invalid format'


        if not re.search(regex,row['email']):
            dict['email'] = 'Invalid Email'


        if (not row['current_salary'].replace('.', '', 1).isdigit()) and row['current_salary'] > '9999':
            dict['current_salary'] = 'Invalid Amount'


        if not row['expected_salary_percentage'].replace('.', '', 1).isdigit():
            dict['expected_salary_percentage'] = 'Not Numeric'


        if (not row['expected_salary_amt'].replace('.', '', 1).isdigit()) and row['expected_salary_amt'] > '9999':
                dict['expected_salary_amt'] = 'Invalid Amount'

        if not row['notice_period'].replace('.', '', 1).isdigit():
            dict['notice_period'] = 'Not Numeric'


        if row['current_status'] != 3:

            if row['interview_date'] < row['date_cv_submitted']:
                dict['interview_date'] = 'Should be after cv submitted'
                row['reason'] = dict

            if row['Int_Tele_Date'] < row['interview_date']:
                dict['Int_Tele_Date'] = 'Should be after interview date'
                row['reason'] = dict

            if row['Int_p1_Date'] < row['interview_date']:
                dict['Int_p1_Date'] = 'Should be after interview date'
                row['reason'] = dict

            if row['Int_p2_Date'] < row['Int_p1_Date']:
                dict['Int_p2_Date'] = 'Should be after p1'
                row['reason'] = dict

            if row['Int_p3_Date'] < row['Int_p2_Date']:
                dict['Int_p3_Date'] = 'Should be after p2'
                row['reason'] = dict

            if row['Int_Final_Date'] < row['Int_p3_Date']:
                dict['Int_Final_Date'] = 'Should be after p3'
                row['reason'] = dict

            if row['Int_Final_Date'] != None:
                if row['Int_HR_Date'] < row['Int_Final_Date']:
                    dict['Int_HR_Date'] = 'Should be after final date'
                    row['reason'] = dict
            else:
                if row['Int_HR_Date'] < row['interview_date']:
                    dict['Int_HR_Date'] = 'Should be after interview date'
                    row['reason'] = dict

            if row['offer_date'] < row['Int_Final_Date'] or row['offer_date'] < row['interview_date'] :
                dict['offer_date'] = 'Should be after final/interview date'
                row['reason'] = dict

            if row['joining_date'] < row['offer_date']:
                dict['joining_date'] = 'Should be after offer date'
                row['reason'] = dict

        # if row['offer_amt'] != None:
        if (not row['offer_amt'].replace('.', '', 1).isdigit()) and row['offer_amt'] < '9999':
            dict['offer_amt'] = 'Invalid Amount'


        row['reason'] = dict

    bad = df.loc[df['reason'] != {}]
    good = df.loc[df['reason'] == {}]
    return HttpResponse(bad.to_html())
