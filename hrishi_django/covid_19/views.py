from django.shortcuts import render

import pandas as pd
import numpy as np
from numpy.random import randn
import matplotlib.pyplot as plt
from datetime import datetime
import os
from django.contrib.auth.models import User,auth

STATE_UT_LIST = [   
                'Delhi',
                'Andaman and Nicobar Islands',
                 'Andhra Pradesh',
                 'Arunachal Pradesh',
                 'Assam',
                 'Bihar',
                 'Chandigarh',
                 'Chhattisgarh',
                 'Dadra and Nagar Haveli and Daman and Diu',
                 'Goa',
                 'Gujarat',
                 'Haryana',
                 'Himachal Pradesh',
                 'Jammu and Kashmir',
                 'Jharkhand',
                 'Karnataka',
                 'Kerala',
                 'Ladakh',
                 'Madhya Pradesh',
                 'Maharashtra',
                 'Manipur',
                 'Meghalaya',
                 'Mizoram',
                 'Nagaland',
                 'Odisha',
                 'Puducherry',
                 'Punjab',
                 'Rajasthan',
                 'Sikkim',
                 'Tamil Nadu',
                 'Telangana',
                 'Tripura',
                 'Uttarakhand',
                 'Uttar Pradesh',
                 'West Bengal'
                 ]

def increment_count_on_search():
    f = open('covid_19/temp_data/all_count_data.txt',"r")
    data = f.read()
    updated_data = int(data)+1
    f = open('covid_19/temp_data/all_count_data.txt',"w")
    f.write(str(updated_data))

    
def process_data():
    increment_count_on_search()
    date = datetime.now().date()
    print(datetime.now())
    file_name = str(date)+".csv"
    bool = os.path.isfile('covid_19/temp_data/'+file_name)
    if bool == True:
        pass
    else:
        data_moh= pd.read_html('https://www.mohfw.gov.in/')
        data_state = data_moh[0][:36]
        data_state.fillna(value=0,inplace=True)
        data_state.rename(columns={'Active Cases*': 'Active Cases', 'Cured/Discharged/Migrated*': 'Cured','Deaths**':'Deaths','Total Confirmed cases*':'Total Confirmed Cases'}, inplace=True)
        data_state[['Active Cases','Cured','Deaths','Total Confirmed Cases']]=data_state[['Active Cases','Cured','Deaths','Total Confirmed Cases']].astype(float)
        data_state.drop(['S. No.'],axis=1)
        data_state.set_index('Name of State / UT',inplace=True)
        data_state.to_csv('covid_19/temp_data/'+file_name)
    
    data = pd.read_csv('covid_19/temp_data/'+file_name)
    return(data)
    

def get_searched_data(search_by,data_state):
    data_searched = data_state[data_state['Name of State / UT'] == search_by]
    data_searched = data_searched.values.tolist()
    data_dict = {}
    data_dict['Deaths'] = int(data_searched[0][4])
    data_dict['Active_Cases']= int(data_searched[0][2])
    data_dict['Cured'] = int(data_searched[0][3])
    data_dict['Total_Confirmed_cases'] = int(data_searched[0][5])
    return(data_dict)

def get_total_cases_india(data_state):
    final_total_cases = {}
    total_cases = {}
    total_cases = data_state[['Active Cases','Cured','Deaths','Total Confirmed Cases']].sum()
    total_cases = total_cases.to_dict()
    final_total_cases['Total_active_cases'] = int(total_cases.get('Active Cases'))
    final_total_cases['Total_cured'] = int(total_cases.get('Cured'))
    final_total_cases['Total_deaths'] = int(total_cases.get('Deaths'))
    final_total_cases['Total_confirmed_cases'] = int(total_cases.get('Total Confirmed Cases'))
    return(final_total_cases)
       
def seek_and_process_data(state):
    data_state = process_data()
    state_data_searched = get_searched_data(state,data_state)
    total_cases_inida = get_total_cases_india(data_state)
    return(state_data_searched,total_cases_inida)

def covid19(request):
    context = {}    
    context['state_list'] = STATE_UT_LIST
    if request.method == 'POST':
        data = request.POST
        state = data.get('state')
        state_data,total_data = seek_and_process_data(state)
        context['state_data'] = state_data
        context['total_data'] = total_data
        context['searched_state'] = state
        
        return render(request, 'covid_19/covid_home.html', context)
    else:
        return render(request, 'covid_19/covid_home.html', context)
    
def view_in_graph(request):
    context = {}
    context['state_list'] = STATE_UT_LIST

    if request.user.is_authenticated:
        searched_state ={}
        final_total_cases = {}
        if request.method == 'POST':
            data = request.POST
            searched_state['state'] = data['state']
            searched_state['Deaths'] = data['Deaths']
            searched_state['Active_Cases'] = data['Active_Cases']
            searched_state['Cured'] = data['Cured']
            searched_state['Total_Confirmed_cases'] = data['Total_Confirmed_cases']
            
            final_total_cases['Total_active_cases'] = data.get('Total_active_cases')
            final_total_cases['Total_cured'] = data.get('Total_cured')
            final_total_cases['Total_deaths'] = data.get('Total_deaths')
            final_total_cases['Total_confirmed_cases'] = data.get('Total_confirmed_cases')
            
            context['state_data'] = searched_state
            context['total_data'] = final_total_cases
            return render(request, 'covid_19/covid_analytics.html', context)
        else:
             return render(request, 'covid_19/covid_home.html', context)
    else:
        context['error']="You must be logged in to view this! Please Register/Login"
        return render(request, 'covid_19/covid_home.html', context)

