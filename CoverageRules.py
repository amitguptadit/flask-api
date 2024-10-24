# ###########################################################################
#  This code contains copyright information which is the proprietary property
#  of # OPTUM Global Solutions. No part of this code may be reproduced,
#  stored or transmitted in any form without the prior written permission of
#  # OPTUM Global Solutions.
#
# Copyright © # OPTUM Global Solutions 2020-2021
# Confidential. All rights reserved.
# ############################################################################

# import unittest

import pandas as pd
# import try_catch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as expect_cond
from selenium.common.exceptions import NoSuchElementException
import time
import config
from selenium.webdriver.support.wait import WebDriverWait

from src.service.util.PdmLogger import PdmLogger
# ######################################
# SCREEN-8 Automation
# The Class CoverageRules.
# @author Amit Gupta
# ######################################
from src.service.util.VisionDb import VisionDb


class CoverageRules:

    def __init__(self, web_driver, rows, worker):
        self.driver = web_driver
        self.row = rows
        self.pdm_worker = worker

    def is_adult_exam(self):
        """ Returns true or false on basis of
        the column CI values by sheet name
        for specific column header and row index .
        Parameters:''.
        Returns:
            column_ad_ci (str):true for The Adult Exam-column CI values.
        """

        benefits_pkg_type = config.benefit_package_plans
        print("CoverageRules # is_adult_exam()#benefits_pkg_type:", benefits_pkg_type)
        if 'Adult Exam' in benefits_pkg_type:
            str_adult_exam = 'true'
            return str_adult_exam
        else:
            str_adult_exam = 'false'
            return str_adult_exam
    pass

    def navigate_to_product_definition_module(self, prod_name):
        """ Automation for Navigate to the application
        SCREEN-1 'Product Components' page from homepage.
        Parameters:
            self :Default.
            prod_name :Product name.
        Returns: ''
        """
        try:
            element = WebDriverWait(self.driver, 10).until(expect_cond.element_to_be_clickable((By.XPATH, "//*[@id='ctl00_oMenu_GlobalMenu_0']")))
            element.click()
        except NoSuchElementException as e:
            self.driver.find_element_by_xpath("//*[@id='ctl00_oMenu_GlobalMenu_0']").click()
        time.sleep(2)
        # ##########[  CLICK DROP DOWN LIST - 'Setup Modules' ]####################
        # 'Setup Modules'
        try:
            element = WebDriverWait(self.driver, 10).until(expect_cond.element_to_be_clickable((By.XPATH, "//td[nobr='Setup Modules']")))
            element.click()
        except NoSuchElementException as e:
            self.driver.find_element_by_xpath("//td[nobr='Setup Modules']").click()

        time.sleep(1)
        # #######[ DRAG MOUSE TO LOCATION - 'Product Definition Module (PDM)' ITEM  ]#######
        # 'Product Definition Module (PDM)'
        try:
            element = WebDriverWait(self.driver, 10).until(expect_cond.element_to_be_clickable((By.XPATH, "//td[nobr='Product Definition Module (PDM)']")))
            element.click()
        except NoSuchElementException as e:
            self.driver.find_element_by_xpath("//td[nobr='Product Definition Module (PDM)']").click()

        # ##################[   NEXT PAGE Benefit Plans ]########################################
        # Benefit Plans
        self.driver.find_element_by_xpath("//select[@id='ctl00_MainContent_ddlMarket']/option[text()='Vision']").click()
        xpath_insurer = "//select[@id='ctl00_MainContent_ddlInsurer']/option[text()='UnitedHealth Group, Inc.']"
        self.driver.find_element_by_xpath(xpath_insurer).click()

        # ######[   RULE -ADDED    ]###############
        is_xpath_element = None
        try:
            # prod_name = 'Test05'
            xpath_prod = "//select[@id='ctl00_MainContent_ddlProduct']/option[text()='"+prod_name+"']"
            xpath_element = self.driver.find_element_by_xpath(xpath_prod)
            xpath_element.click()
        except NoSuchElementException as e:
            print("Element Not present ", e)
            is_xpath_element = 'NA'

        if is_xpath_element == 'NA':
            # ######[  GO FOR CREATE NEW PRODUCT    ]###############
            pass
        else:
            # #######[   CLICK LINK TO NAVIGATE NEXT PAGE SCREEN-1 'Product Components'  ]######
            print("[   CLICK LINK TO NAVIGATE NEXT PAGE SCREEN-1 'Product Components'  ]")
            self.driver.find_element_by_xpath("//a[@id='ctl00_MainContent_btnSelect']").click()
            pass
        # ######[   END BLOCK 'RULE -ADDED'    ]###############
        # ###############################################
        pass

    # ####################################################################################
    # #############[ NAVIGATION TO SCREEN-8 'Coverage Rules' ############
    # #####################################################################################
    def navigation_to_coverage_rules(self, prod_name, nav_to_next_screen):
        """ NAVIGATION TO SCREEN-8 'Coverage Rules'.
        Parameters:
            self :Default.
            prod_name :Product name.
            nav_to_next_screen : 'bool' flag to navigate next screen 'Patient Pay Attributes'
        Returns: ''
        """
        print("[navigation_to_coverage_rules()# prod_name :", prod_name,
              "#nav_to_next_screen :" + str(nav_to_next_screen) + "]")

        logs = "[CoverageRules:navigation_to_coverage_rules()#pdm_worker:" + self.pdm_worker +\
               "#prod_name :" + prod_name + "]"
        PdmLogger.instance().configure_logger().info(logs)
        # ###########[ CLICK 'Benefits' TYPE MENU ]######################
        time.sleep(1)

        # benefit_level_name = ['In Network', 'Out of Network']
        benefit_level_name = list(config.list_of_benefit_level)
        logs = "[CoverageRules:navigation_to_coverage_rules()#pdm_worker:" + self.pdm_worker +\
               "# prod_name :" + prod_name + "#list benefit_level_name :" + str(benefit_level_name) + "]"
        PdmLogger.instance().configure_logger().info(logs)
        for i in range(len(benefit_level_name)):
            try:
                bnf_name = benefit_level_name[i]

                logs = "[CoverageRules:navigation_to_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                       "# prod_name :" + prod_name + "#benefit_level_name :" + str(bnf_name) + "]"
                PdmLogger.instance().configure_logger().info(logs)

                res = self.create_coverage_rules(prod_name, bnf_name)

                if(res == 'fail'):
                    return 'fail'

            except NoSuchElementException as e:
                print("navigation_to_coverage_rules()#Element Not present ", e)
                logs = "[CoverageRules:navigation_to_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                       "# prod_name :" + prod_name + "#Exception is :" + str(e) + "]"
                PdmLogger.instance().configure_logger().error(logs)
                return 'fail'
                pass
        pass


    def get_prod_details(self, prod_name, benefit_level_name, screen_name, conn, benefit_codeset):
        """ Automation for 'MATERIAL PLAN CODE SET VALUES' .
        Parameters:
            self :Default.
            prod_name :Product name.
            benefit_level_name : benefit_level_name.
            screen_name : screen_name
            conn : Db Connection
        Returns: ''
        """
        try:
            prod_summery_details = {}  # prod_summery_details

            logs = "[CoverageRules:get_prod_details()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name:" + prod_name + \
                   "#benefit_level_name:" + benefit_level_name + "#screen_name:" + screen_name + "#benefit_codeset:" + benefit_codeset + " ]"
            PdmLogger.instance().configure_logger().info(logs)

            product_id = ''
            product_period = ''
            benefit_level = ''
            codeset_id = ''

            query = "SELECT PRODUCT_ID FROM enterprisedb.[dbo].PRODUCTS WHERE NAME = '" + prod_name + "'"
            logs = "[CoverageRules:get_prod_details()# query=" + query + " ]"
            PdmLogger.instance().configure_logger().info(logs)
            dfs = pd.read_sql_query(query, conn)
            for index, row in dfs.iterrows():
                product_id = str(row['PRODUCT_ID'])
                prod_summery_details['PRODUCT_ID'] = product_id
            pass
            """
            querySelect = "SELECT * FROM UserDb.[dbo].VISION_PRODUCT_MASTER  WHERE NAME = '" + prod_name + "'"
            dfs = pd.read_sql_query(querySelect, conn)
            for index, row in dfs.iterrows():
                REQUEST_TYPE = str(row['REQUEST_TYPE'])
            """
            REQUEST_TYPE = str(self.row['REQUEST_TYPE'])
            logs = "[CoverageRules:get_prod_details()# REQUEST_TYPE=" + REQUEST_TYPE + "#prod_name:" + prod_name + " ]"
            PdmLogger.instance().configure_logger().info(logs)

            effective_date = str(self.row['EFFECTIVE_DATE'])
            if product_id != '' and (
                    'BUILD_NEW_MAP_NEW' in REQUEST_TYPE or 'BUILD_NEW_MAP_CHANGE' in REQUEST_TYPE or 'BUILD_NEW_MAP_REPLACE' in REQUEST_TYPE or 'PRODUCT_RETRO_CHANGE' in REQUEST_TYPE):
                # query = "SELECT PRODUCT_PERIOD FROM enterprisedb.[dbo].PRODUCT_PERIODS WHERE PRODUCT_ID = " + product_id + " AND EFFECTIVE_DATE = '1980-01-01' AND (TERMINATION_DATE IS NULL)"
                query = "SELECT PRODUCT_PERIOD FROM enterprisedb.[dbo].PRODUCT_PERIODS WHERE PRODUCT_ID = " + product_id + " AND EFFECTIVE_DATE = '"+effective_date+"'"
                logs = "[CoverageRules:get_prod_details()# query=" + query + "#prod_name:" + prod_name +" ]"
                PdmLogger.instance().configure_logger().info(logs)
                dfs = pd.read_sql_query(query, conn)
                for index, row in dfs.iterrows():
                    product_period = str(row['PRODUCT_PERIOD'])
                    prod_summery_details['PRODUCT_PERIOD'] = product_period
                    logs = "[CoverageRules:get_prod_details_ifcondition()# query=" + query + " #product_period: " + product_period + " #REQUEST_TYPE: " + REQUEST_TYPE + "#prod_name:" + prod_name +" ]"
                    PdmLogger.instance().configure_logger().info(logs)
                pass
            else:
                if product_id != '' and ('PRODUCT_PERIOD_CHANGE' in REQUEST_TYPE):
                    query = "SELECT MAX(PRODUCT_PERIOD) PRODUCT_PERIOD FROM enterprisedb.[dbo].PRODUCT_PERIODS WHERE PRODUCT_ID = " + product_id + " AND (TERMINATION_DATE IS NULL)"
                    logs = "[CoverageRules:get_prod_details()# query=" + query + "#prod_name:" + prod_name +" ]"
                    PdmLogger.instance().configure_logger().info(logs)
                    dfs = pd.read_sql_query(query, conn)
                    for index, row in dfs.iterrows():
                        product_period = str(row['PRODUCT_PERIOD'])
                        prod_summery_details['PRODUCT_PERIOD'] = product_period
                        logs = "[CoverageRules:get_prod_details_elsecondition()# query=" + query + " #product_period: " + product_period + " #REQUEST_TYPE: " + REQUEST_TYPE + "#prod_name:" + prod_name +"]"
                        PdmLogger.instance().configure_logger().info(logs)
                    pass
                pass
            if product_period != '':
                query = "SELECT PRODUCT_ID, PRODUCT_PERIOD, BENEFIT_LEVEL FROM enterprisedb.[dbo].PRODUCT_BENEFIT_LEVELS WHERE PRODUCT_ID = " + product_id + " AND DESCRIPTION = '" + benefit_level_name + "' AND PRODUCT_PERIOD = " + product_period + ""
                logs = "[CoverageRules:get_prod_details()# query=" + query +"#prod_name:" + prod_name +" ]"
                PdmLogger.instance().configure_logger().info(logs)
                dfs = pd.read_sql_query(query, conn)
                for index, row in dfs.iterrows():
                    benefit_level = str(row['BENEFIT_LEVEL'])
                    prod_summery_details['BENEFIT_LEVEL'] = benefit_level
                pass
            logs = "[CoverageRules:get_prod_details()# query=" + str(prod_summery_details) +"#prod_name:" + prod_name +" ]"
            PdmLogger.instance().configure_logger().info(logs)

            return prod_summery_details
        except NoSuchElementException as e:
            logs = "[CoverageRules:get_prod_details()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name :" + prod_name + "#NoSuchElementException :" + str(e) + "]"
            PdmLogger.instance().configure_logger().error(logs)
            return 'fail'
        except Exception as ex:
            logs = "[CoverageRules:get_prod_details()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name :" + prod_name + "#Exception :" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)
            return 'fail'
    pass
    # ####################################################################################
    # #############[ SCREEN-8 'Coverage Rules' ############
    # #####################################################################################
    def create_coverage_rules(self, prod_name, benefit_level_name):
        """ CREATE COVERAGE RULES FOR SCREEN-8 'Coverage Rules'.
        Parameters:
            self :Default.
            prod_name :Product name.
            benefit_level_name :Benefit level name.
        Returns: ''
        """
        # benefit_level_name = ['In Network', 'Out of Network']
        try:

            # ##############[ 5june2020 ]#####################
            dependent_age_limit_info = str(self.row['DEPENDENT_AGE_LIMIT_INFO'])
            if pd.isna(dependent_age_limit_info) or dependent_age_limit_info == 'nan' \
                    or dependent_age_limit_info == 'NaN' \
                    or dependent_age_limit_info == 'None' or dependent_age_limit_info == '' \
                    or dependent_age_limit_info == '0.00' or dependent_age_limit_info == '0' \
                    or dependent_age_limit_info == '0.0' or dependent_age_limit_info == 'NULL':
                dependent_age_limit_info = ''
            # ##[ 'dependent_age_limit_info' 0-18 then update age  ]##
            config.dependent_age_limit = dependent_age_limit_info

            benefits_pkg_type = str(config.benefit_package_plans)
            same_copay_coinsurance = 'share same coinsurance or copay'
            str_copay_insurance = str(config.copay_insurance)
            is_no_benefit_for_oon = str(config.is_no_benefit_for_oon)

            logs = "[CoverageRules:create_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                   "#benefits_pkg_type:" + str(benefits_pkg_type) +\
                   "#dependent_age_limit_info:" + str(dependent_age_limit_info) +\
                   "#is_same_copay_coinsurance:" + str_copay_insurance +\
                   "#is_no_benefit_for_oon:" + is_no_benefit_for_oon + "]"
            PdmLogger.instance().configure_logger().info(logs)
            str_match_case_id = '0'
            conn = VisionDb()
            conn = conn.connect_dbs()
            if conn != 1:
                screen_name = 'coverage_exclusive'
                benefit_codeset = ''
                prod_summery_details = self.get_prod_details(prod_name, benefit_level_name, screen_name, conn,
                                                             benefit_codeset)
                if(prod_summery_details == 'fail'):
                    return 'fail'
                product_id = prod_summery_details['PRODUCT_ID']
                product_period = prod_summery_details['PRODUCT_PERIOD']
                benefit_level = prod_summery_details['BENEFIT_LEVEL']
                if (benefits_pkg_type == 'Exam Only' or benefits_pkg_type == 'EHB Exam Only') \
                        and is_no_benefit_for_oon == 'false'  \
                        and 'In Network' in benefit_level_name \
                        and 'In Network - No CL Formulary' not in benefit_level_name:
                    str_match_case_id = '1'
                    res = self.in_network_not_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id,
                                                                  product_period, benefit_level, conn)
                    if(res== 'fail'):
                        return 'fail'

                elif (benefits_pkg_type == 'Exam Only' or benefits_pkg_type == 'EHB Exam Only') \
                        and is_no_benefit_for_oon == 'true' \
                        and 'In Network' in benefit_level_name \
                        and 'In Network - No CL Formulary' not in benefit_level_name:
                    str_match_case_id = '2'
                    res = self.in_network_not_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id,
                                                                  product_period, benefit_level, conn)
                    if (res == 'fail'):
                        return 'fail'
                elif (benefits_pkg_type == 'Exam Only' or benefits_pkg_type == 'EHB Exam Only') \
                        and is_no_benefit_for_oon == 'false' \
                        and 'Out of Network' in benefit_level_name:
                    str_match_case_id = '3'
                    res = self.in_network_not_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id,
                                                                  product_period, benefit_level, conn)
                    if (res == 'fail'):
                        return 'fail'
                elif (benefits_pkg_type == 'Exam Only' or benefits_pkg_type == 'EHB Exam Only') \
                        and is_no_benefit_for_oon == 'true' and 'Out of Network' in benefit_level_name:
                    str_match_case_id = '4'
                    res = self.in_network_not_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id,
                                                                  product_period, benefit_level, conn)
                    if (res == 'fail'):
                        return 'fail'
                elif benefits_pkg_type == 'EHB + Pediatric Low Vision' and is_no_benefit_for_oon == 'false'\
                        and ('In Network' in benefit_level_name or 'In Network - No CL Formulary' in benefit_level_name):
                    str_match_case_id = '5'
                    if dependent_age_limit_info == '0-18':
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '18',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-19':
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '19',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-20':
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '20',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-21':
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '21',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-24':
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '24',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    # added by Gaurav
                    elif dependent_age_limit_info == '0-26':
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '26',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    else:
                        logs = "[CoverageRules:create_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                               "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                               "#NOT ADDED due to not match dependent_age_limit_info:" + dependent_age_limit_info +\
                               "str_match_case_id:" + str_match_case_id + "]"
                        PdmLogger.instance().configure_logger().error(logs)
                        return 'fail'
                elif benefits_pkg_type == 'EHB + Pediatric Low Vision' and is_no_benefit_for_oon == 'true'\
                        and ('In Network' in benefit_level_name or 'In Network - No CL Formulary' in benefit_level_name):
                    str_match_case_id = '6'
                    if dependent_age_limit_info == '0-18':
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '18',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-19':
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '19',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-20':
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '20',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-21':
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '21',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-24':
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '24',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    #added by Gaurav
                    elif dependent_age_limit_info == '0-26':
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '26',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    else:
                        logs = "[CoverageRules:create_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                               "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                               "#NOT ADDED due to not match dependent_age_limit_info:" + dependent_age_limit_info + \
                               "str_match_case_id:" + str_match_case_id + "]"
                        PdmLogger.instance().configure_logger().error(logs)
                        return 'fail'
                elif benefits_pkg_type == 'EHB + Pediatric Low Vision' \
                        and (is_no_benefit_for_oon == 'true' or is_no_benefit_for_oon == 'false') \
                        and 'Out of Network' in benefit_level_name:
                    str_match_case_id = '7'
                    # DONE
                    if dependent_age_limit_info == '0-18':
                        res= self.out_of_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name,
                                                                                     '18', product_id, product_period,
                                                                                     benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-19':
                        res= self.out_of_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name,
                                                                                     '19', product_id, product_period,
                                                                                     benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-20':
                        res= self.out_of_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name,
                                                                                     '20', product_id, product_period,
                                                                                     benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-21':
                        res= self.out_of_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name,
                                                                                     '21', product_id, product_period,
                                                                                     benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-24':
                        res= self.out_of_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name,
                                                                                     '24', product_id, product_period,
                                                                                     benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'

                    #added by Gaurav
                    elif dependent_age_limit_info == '0-26':
                        res= self.out_of_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name,
                                                                                     '26', product_id, product_period,
                                                                                     benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    else:
                        logs = "[CoverageRules:create_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                               "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                               "#NOT ADDED due to not match dependent_age_limit_info:" + dependent_age_limit_info + \
                               "str_match_case_id:" + str_match_case_id + "]"
                        PdmLogger.instance().configure_logger().error(logs)
                        return 'fail'

                elif (benefits_pkg_type == 'EHB + Pediatric Low Vision + Adult Exam' or 'EHB + Pediatric Low Vision + Adult Exam' in benefits_pkg_type) \
                        and (is_no_benefit_for_oon == 'false' or is_no_benefit_for_oon == 'true') \
                        and ('In Network' in benefit_level_name or 'In Network - No CL Formulary' in benefit_level_name)\
                        and str_copay_insurance == same_copay_coinsurance:
                    str_match_case_id = '8'
                    # DONE
                    res = self.in_network_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id, product_period,
                                                              benefit_level, conn)
                    if(res == 'fail'):
                        return 'fail'
                elif (benefits_pkg_type == 'EHB + Pediatric Low Vision + Adult Exam' or 'EHB + Pediatric Low Vision + Adult Exam' in benefits_pkg_type) \
                        and (is_no_benefit_for_oon == 'false' or is_no_benefit_for_oon == 'true')\
                        and 'Out of Network' in benefit_level_name \
                        and str_copay_insurance == same_copay_coinsurance:
                    str_match_case_id = '9'
                    # DONE
                    res = self.out_of_network_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id,
                                                                  product_period, benefit_level, conn)
                    if (res == 'fail'):
                        return 'fail'
                    benefit_level_type_1 = ['In Network', 'Out of Network']

                elif (benefits_pkg_type == 'EHB + Pediatric Low Vision + Adult Exam' or 'EHB + Pediatric Low Vision + Adult Exam' in benefits_pkg_type) and \
                        (is_no_benefit_for_oon == 'true' or is_no_benefit_for_oon == 'false') \
                        and ('In Network(0-18)' in benefit_level_name or
                             'In Network - No CL Formulary(0-18)' in benefit_level_name or
                             'In Network (Age 0-19)' in benefit_level_name or
                             'In Network - No CL Formulary (Age 0-19)' in benefit_level_name or 'In Network(19+)' in benefit_level_name or
                             'In Network - No CL Formulary(19+)' in benefit_level_name or
                             'In Network (Age 20+)' in benefit_level_name or
                             'In Network - No CL Formulary (Age 20+)' in benefit_level_name or
                             #added by gaurav - next line
                             'In Network (Age 0-26)' in benefit_level_name) \
                        and str_copay_insurance != same_copay_coinsurance:
                    str_match_case_id = '10'

                    age_range = ''
                    if dependent_age_limit_info == '0-18':
                        age_range = '18'
                    elif dependent_age_limit_info == '0-19':
                        age_range = '19'
                    elif dependent_age_limit_info == '0-20':
                        age_range = '20'
                    elif dependent_age_limit_info == '0-21':
                        age_range = '21'
                    elif dependent_age_limit_info == '0-24':
                        age_range = '24'
                    # added by gaurav
                    elif dependent_age_limit_info == '0-26':
                        age_range = '26'

                    logs = "[CoverageRules:create_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                           "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) \
                           + "str_match_case_id:" + str_match_case_id + "ages is:"+age_range+\
                           "#dependent_age_limit_info:" + dependent_age_limit_info + "]"
                    PdmLogger.instance().configure_logger().info(logs)

                    if ('In Network(0-18)' in benefit_level_name or 'In Network (Age 0-19)' or 'In Network (Age 0-26)' in benefit_level_name or 'In Network - No CL Formulary(0-18)' in benefit_level_name or  'In Network - No CL Formulary (Age 0-19)' in benefit_level_name ):
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name,
                                                                                       age_range,
                                                                                       product_id, product_period,
                                                                                       benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                        # 1july2021
                    elif ('In Network(19+)' in benefit_level_name or 'In Network (Age 20+)' in benefit_level_name or 'In Network - No CL Formulary(19+)' in benefit_level_name or 'In Network - No CL Formulary (Age 20+)' in benefit_level_name):
                        res = self.in_network_19_plus_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id,
                                                                      product_period, benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    else:
                        logs = "[CoverageRules:create_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                               "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                               "#NOT ADDED due to not match dependent_age_limit_info:" + dependent_age_limit_info + \
                               "str_match_case_id:" + str_match_case_id + "]"
                        PdmLogger.instance().configure_logger().error(logs)
                        return 'fail'
                elif (benefits_pkg_type == 'EHB + Pediatric Low Vision + Adult Exam' or 'EHB + Pediatric Low Vision + Adult Exam' in benefits_pkg_type) and \
                        (is_no_benefit_for_oon == 'true' or is_no_benefit_for_oon == 'false') \
                        and 'Out of Network' in benefit_level_name and str_copay_insurance != same_copay_coinsurance:
                    str_match_case_id = '12'
                    # DONE
                    res = self.out_of_network_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id,
                                                                  product_period, benefit_level, conn)
                    if (res == 'fail'):
                        return 'fail'
                    benefit_level_type_1 = ['In Network', 'Out of Network']

                elif benefits_pkg_type == 'EHB' and (is_no_benefit_for_oon == 'true' or is_no_benefit_for_oon == 'false') \
                         and ('In Network' in benefit_level_name or 'In Network - No CL Formulary' in benefit_level_name or 'Out of Network' in benefit_level_name):
                    str_match_case_id = '13'
                    # DONE
                    res = self.in_network_not_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id,
                                                                  product_period, benefit_level, conn)
                    if (res == 'fail'):
                        return 'fail'
                elif (benefits_pkg_type == 'EHB + Adult Exam' or 'EHB + Adult Exam' in benefits_pkg_type) \
                        and 'In Network' in benefit_level_name and str_copay_insurance != same_copay_coinsurance:
                    str_match_case_id = '14'
                    # DONE
                    # ******************************
                    if ('In Network - No CL Formulary' not in benefit_level_name):
                        res = self.in_network_not_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id,
                                                                            product_period, benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                        # 1july2021
                    elif ('In Network - No CL Formulary' in benefit_level_name):
                        age_range = ''
                        if dependent_age_limit_info == '0-18':
                            age_range = '18'
                        elif dependent_age_limit_info == '0-19':
                            age_range = '19'
                        elif dependent_age_limit_info == '0-20':
                            age_range = '20'
                        elif dependent_age_limit_info == '0-21':
                            age_range = '21'
                        elif dependent_age_limit_info == '0-24':
                            age_range = '24'
                        res = self.in_network_19_plus_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id,
                                                                      product_period, benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                elif (benefits_pkg_type == 'EHB + Adult Exam' or 'EHB + Adult Exam' in benefits_pkg_type) \
                        and is_no_benefit_for_oon == 'false' and 'Out of Network' in benefit_level_name \
                        and str_copay_insurance != same_copay_coinsurance:
                    str_match_case_id = '17'
                    # DONE
                    res = self.in_network_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id, product_period,
                                                              benefit_level, conn)
                    if (res == 'fail'):
                        return 'fail'
                elif (benefits_pkg_type == 'EHB + Adult Exam' or 'EHB + Adult Exam' in benefits_pkg_type) \
                        and is_no_benefit_for_oon == 'true' \
                        and 'Out of Network' in benefit_level_name and str_copay_insurance != same_copay_coinsurance:
                    str_match_case_id = '18'
                    # DONE
                    res = self.in_network_not_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id,
                                                                  product_period, benefit_level, conn)
                elif (benefits_pkg_type == 'EHB + Adult Exam' or 'EHB + Adult Exam' in benefits_pkg_type) \
                        and is_no_benefit_for_oon == 'true' and 'Out of Network' in benefit_level_name \
                        and str_copay_insurance == same_copay_coinsurance:
                    str_match_case_id = '19'
                    # DONE
                    res = self.in_network_not_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id,
                                                                  product_period, benefit_level, conn)
                    if (res == 'fail'):
                        return 'fail'
                elif (benefits_pkg_type == 'EHB + Adult Exam' or 'EHB + Adult Exam' in benefits_pkg_type)\
                        and is_no_benefit_for_oon == 'false' \
                        and 'Out of Network' in benefit_level_name and str_copay_insurance == same_copay_coinsurance:
                    str_match_case_id = '20'
                    # DONE
                    res = self.in_network_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id, product_period,
                                                              benefit_level, conn)
                    if (res == 'fail'):
                        return 'fail'
                elif (benefits_pkg_type == 'EHB + Adult Exam' or 'EHB + Adult Exam' in benefits_pkg_type) \
                        and(is_no_benefit_for_oon == 'true' or is_no_benefit_for_oon == 'false')\
                        and ('In Network(0-18)' in benefit_level_name or
                             'In Network - No CL Formulary(0-18)' in benefit_level_name or
                             'In Network(19+)' in benefit_level_name or
                             'In Network - No CL Formulary(19+)' in benefit_level_name or
                        'In Network (Age 0-19)' in benefit_level_name or
                             'In Network - No CL Formulary (Age 0-19)' in benefit_level_name or
                             'In Network (Age 20+)' in benefit_level_name or
                             'In Network - No CL Formulary (Age 20+)' in benefit_level_name) \
                        and str_copay_insurance == same_copay_coinsurance:
                    str_match_case_id = '21'
                    # DONE
                    res = self.in_network_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id, product_period,
                                                              benefit_level, conn)
                    if (res == 'fail'):
                        return 'fail'
                elif (benefits_pkg_type == 'EHB Exam Only (Pediatric Only)' or 'EHB Exam Only (Pediatric Only)' in benefits_pkg_type)\
                        and (is_no_benefit_for_oon == 'false' or is_no_benefit_for_oon == 'true') \
                        and 'In Network' in benefit_level_name \
                        and 'In Network - No CL Formulary' not in benefit_level_name:
                    str_match_case_id = '22'
                    if dependent_age_limit_info == '0-18':
                        # DONE
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '18',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-19':
                        # DONE
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '19',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-20':
                        # DONE
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '20',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-21':
                        # DONE
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '21',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-24':
                        # DONE
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '24',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    else:
                        print('fail')
                elif (benefits_pkg_type == 'EHB Exam Only (Pediatric Only)' or 'EHB Exam Only (Pediatric Only)' in benefits_pkg_type)\
                        and is_no_benefit_for_oon == 'false' and 'Out of Network' in benefit_level_name:
                    str_match_case_id = '23'
                    if dependent_age_limit_info == '0-18':
                        # DONE
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '18',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-19':
                        # DONE
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '19',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-20':
                        # DONE
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '20',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-21':
                        # DONE
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '21',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    elif dependent_age_limit_info == '0-24':
                        # DONE
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '24',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                    else:
                        # DONE
                        res = self.in_network_not_adult_exam_coverage_rules_member_age(prod_name, benefit_level_name, '18',
                                                                                 product_id, product_period,
                                                                                 benefit_level, conn)
                        if (res == 'fail'):
                            return 'fail'
                elif (benefits_pkg_type == 'EHB Exam Only (Pediatric Only)' or 'EHB Exam Only (Pediatric Only)' in benefits_pkg_type)\
                        and is_no_benefit_for_oon == 'true' and 'Out of Network' in benefit_level_name:
                    str_match_case_id = '24'
                    # DONE
                    res = self.in_network_not_adult_exam_coverage_rules(prod_name, benefit_level_name, product_id,
                                                                  product_period, benefit_level, conn)
                    if (res == 'fail'):
                        return 'fail'
                # #######################[ Need To Work ]############################
                logs = "[CoverageRules:create_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                       "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                       "#benefits_pkg_type:" + str(benefits_pkg_type) + \
                       "#str_match_case_id:" + str(str_match_case_id) + "#product_id:" + str(product_id) +\
                       "#product_period:" + str(product_period) + "#benefit_level:" + str(benefit_level) + "]"
                PdmLogger.instance().configure_logger().info(logs)
            conn.close()
        except NoSuchElementException as e:
            print("create_coverage_rules()#Element Not present ", e)
            logs = "[CoverageRules:create_coverage_rules()#pdm_worker:" + self.pdm_worker +\
                   "# prod_name :" + prod_name + "#Element Not present :" + str(e) + "]"
            PdmLogger.instance().configure_logger().error(logs)
            return 'fail'
            pass
    pass

    def in_network_adult_exam_coverage_rules(self, prod_name, benefit_level_name, product_id, product_period,
                                             benefit_level, conn):
        """ ADDING COVERAGE RULES WHEN IN-NETWORK,ADULT EXAM FOR 'Coverage Rules' SCREEN -8.2.
        Parameters:
            self :Default.
            prod_name :Product name.
            benefit_level_name :Benefit level name.
        Returns: ''
        """
        seq_number = ''

        logs = "[CoverageRules:in_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
               "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + "]"
        PdmLogger.instance().configure_logger().info(logs)

        dependent_age_limit_info = str(config.dependent_age_limit)
        if dependent_age_limit_info == '0-18' \
                or dependent_age_limit_info == '0-19' \
                or dependent_age_limit_info == '0-20' \
                or dependent_age_limit_info == '0-21' \
                or dependent_age_limit_info == '0-24':
            print('ok')
        else:
            logs = "[CoverageRules:in_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                   "#NOT ADDED due to not match dependent_age_limit_info:" + dependent_age_limit_info + "]"
            PdmLogger.instance().configure_logger().error(logs)
            return 'fail'
        try:
            seq_number = 1
            code_set_text = ' Codeset = General Exclusion Codes'
            res = self.adding_codeset_general_exclusion_codes(prod_name, benefit_level_name, product_id, product_period,
                                                        benefit_level, conn, seq_number)
            if(res ==  'fail'):
                return 'fail'

            logs = "[CoverageRules:in_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                   "#dependent_age_limit_info:" + dependent_age_limit_info + "#code_set_text:" + code_set_text + " ]"
            PdmLogger.instance().configure_logger().info(logs)

            age_variable = ''
            if dependent_age_limit_info == '0-21':
                age_variable = '21'
            elif dependent_age_limit_info == '0-24':
                age_variable = '24'
            elif dependent_age_limit_info == '0-20':
                age_variable = '20'
            elif dependent_age_limit_info == '0-19':
                age_variable = '19'
            elif dependent_age_limit_info == '0-18':
                age_variable = '18'
            else:
                logs = "[CoverageRules:in_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                       "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                       "#NOT ADDED due to not match dependent_age_limit_info:" + dependent_age_limit_info + "]"
                PdmLogger.instance().configure_logger().error(logs)
                return 'fail'
            seq_number = 2
            code_set_text = ' Codeset = All Materials + Contact Lens Fit AND Member Age > ' + age_variable
            res = self.adding_codeset_all_materials_contact_lens_fit_and_member_age(prod_name, benefit_level_name,
                                                                                    product_id,
                                                                                    product_period,
                                                                                    benefit_level, conn, seq_number,
                                                                                    age_variable)
            if(res == 'fail'):
                return 'fail'
            logs = "[CoverageRules:in_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                   "#dependent_age_limit_info:" + dependent_age_limit_info + "#code_set_text:" + code_set_text + " ]"
            PdmLogger.instance().configure_logger().info(logs)
            pass
        except NoSuchElementException as e:
            print("in_network_adult_exam_coverage_rules()#Element Not present ", e)
            logs = "[CoverageRules:in_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker +\
                   "#prod_name :" + prod_name + "#Element Not present:" + str(e) + "]"
            PdmLogger.instance().configure_logger().error(logs)
            return 'fail'
            pass
    pass

    def adding_codeset_general_exclusion_codes(self, prod_name, benefit_level_name, product_id, product_period,
                                                 benefit_level, conn, seq_number):
        """ ADDING 'Codeset = General Exclusion Codes' RULE FOR 'Coverage Rules' SCREEN -8.3.
        --COVERAGE RULES
        --1.Codeset = General Exclusion Codes
        Parameters:
            self :Default.
            prod_name :Product name.
            benefit_level_name :Benefit level name.
            product_id : product_id.
            product_period : product_period.
            benefit_level : benefit_level.
            conn : conn.
            seq_number : seq_number.
        Returns: ''
        """
        sql_rule_id = ''
        seq_number = str(seq_number)
        query = "INSERT INTO [EnterpriseDb].[dbo].[SQL_RULES] VALUES (' AND CC.CODESET_ID = 74', ' AND Codeset = General Exclusion Codes',2)"
        logs = "[CoverageRules:adding_codeset_general_exclusion_codes()#prod_name:" + prod_name + \
               "# query 1=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_general_exclusion_codes()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 1 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)

        try:
            query = "SELECT  SCOPE_IDENTITY() sql_rule_id"
            logs = "[CoverageRules:adding_codeset_general_exclusion_codes()#prod_name:" + prod_name + \
                   "# query 2=" + \
                   str(query) + " ]"
            PdmLogger.instance().configure_logger().info(logs)
            dfs = pd.read_sql_query(query, conn)
            for index, row in dfs.iterrows():
                sql_rule_id = str(row['sql_rule_id'])
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_general_exclusion_codes()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 2 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)

        # DONE
        query = "INSERT INTO [EnterpriseDb].[dbo].[SQL_RULE_DETAIL] VALUES (" + sql_rule_id + ", 2,'=', '74', 'CC.CODESET_ID = 74', 'Codeset = General Exclusion Codes')"
        logs = "[CoverageRules:adding_codeset_general_exclusion_codes()#prod_name:" + prod_name + \
               "# query 3=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_general_exclusion_codes()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 3 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)

        query = "INSERT INTO [EnterpriseDb].[dbo].[COVERAGE_RULES] VALUES (" + product_id + "," + product_period + "," + benefit_level + "," + seq_number + ", " + sql_rule_id + ", 0)"
        logs = "[CoverageRules:adding_codeset_general_exclusion_codes()#prod_name:" + prod_name + \
               "# query 4=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_general_exclusion_codes()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 4 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)

    def adding_codeset_all_codes_and_member_age_gt(self, prod_name, benefit_level_name, product_id, product_period,
                                                 benefit_level, conn, seq_number, age_variable):
        """ ADDING 'Codeset = General Exclusion Codes' RULE FOR 'Coverage Rules' SCREEN -8.3.
        --COVERAGE RULES
        --2.Codeset = All Codes AND Member Age > @AGEVARIABLE
        Parameters:
            self :Default.
            prod_name :Product name.
            benefit_level_name :Benefit level name.
            product_id : product_id.
            product_period : product_period.
            benefit_level : benefit_level.
            conn : conn.
            seq_number : seq_number.
            age_variable : age_variable.
        Returns: ''
        """
        seq_number = str(seq_number)
        query = "INSERT INTO [EnterpriseDb].[dbo].[SQL_RULES] VALUES (' AND CC.CODESET_ID = 8 AND CH.AGE > " + age_variable + "', ' AND Codeset = All Codes AND Member Age > " + age_variable + "',2)"
        logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_gt()#prod_name:" + prod_name + \
               "# query 1=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_gt()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 1 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)



        try:
            sql_rule_id = ''
            query = "SELECT  SCOPE_IDENTITY() sql_rule_id"
            logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_gt()#prod_name:" + prod_name + \
                   "# query 2=" + \
                   str(query) + " ]"
            PdmLogger.instance().configure_logger().info(logs)
            dfs = pd.read_sql_query(query, conn)
            for index, row in dfs.iterrows():
                sql_rule_id = str(row['sql_rule_id'])
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_gt()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 2 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)


        # DONE
        query = "INSERT INTO [EnterpriseDb].[dbo].[SQL_RULE_DETAIL] VALUES (" + sql_rule_id + ", 2,'=', '8', 'CC.CODESET_ID = 8', 'Codeset = All Codes'),(" + sql_rule_id + ", 14,'>', '" + age_variable + "', 'CH.AGE > " + age_variable + "', 'Member Age > " + age_variable + "')"
        logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_gt()#prod_name:" + prod_name + \
               "# query 3=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_gt()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 3 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)


        query = "INSERT INTO [EnterpriseDb].[dbo].[COVERAGE_RULES] VALUES (" + product_id + "," + product_period + "," + benefit_level + "," + seq_number + ", " + sql_rule_id + ", 0)"
        logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_gt()#prod_name:" + prod_name + \
               "# query 4=" + str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_gt()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 4 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)


    def adding_codeset_all_codes_and_member_age_lt(self, prod_name, benefit_level_name, product_id, product_period,
                                                 benefit_level, conn, seq_number, age_variable):
        """ ADDING 'Codeset = General Exclusion Codes' RULE FOR 'Coverage Rules' SCREEN -8.3.
        --COVERAGE RULES
        --3.Codeset = All Codes AND Member Age < " + age_variable + "
        Parameters:
            self :Default.
            prod_name :Product name.
            benefit_level_name :Benefit level name.
            product_id : product_id.
            product_period : product_period.
            benefit_level : benefit_level.
            conn : conn.
            seq_number : seq_number.
            age_variable : age_variable.
        Returns: ''
        """
        seq_number = str(seq_number)
        query = "INSERT INTO [EnterpriseDb].[dbo].[SQL_RULES] VALUES (' AND CC.CODESET_ID = 8 AND CH.AGE < " + age_variable + "', ' AND Codeset = All Codes AND Member Age < " + age_variable + "',2)"
        logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_lt()#prod_name:" + prod_name + \
               "#benefit_level_name:" + str(benefit_level_name) + "# query 1=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_lt()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 1 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)


        try:
            sql_rule_id = ''
            query = "SELECT  SCOPE_IDENTITY() sql_rule_id"
            logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_lt()#prod_name:" + prod_name + \
               "# query 2=" + \
               str(query) + " ]"
            PdmLogger.instance().configure_logger().info(logs)
            dfs = pd.read_sql_query(query, conn)
            for index, row in dfs.iterrows():
                sql_rule_id = str(row['sql_rule_id'])
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_lt()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 2 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)


        # DONE
        query = "INSERT INTO [EnterpriseDb].[dbo].[SQL_RULE_DETAIL] VALUES (" + sql_rule_id + ", 2,'=', '8', 'CC.CODESET_ID = 8', 'Codeset = All Codes'),(" + sql_rule_id + ", 14,'<', '" + age_variable + "', 'CH.AGE < " + age_variable + "', 'Member Age < " + age_variable + "')"
        logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_lt()#prod_name:" + prod_name + \
               "# query 3=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_lt()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 3 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)


        query = "INSERT INTO [EnterpriseDb].[dbo].[COVERAGE_RULES] VALUES (" + product_id + "," + product_period + "," + benefit_level + "," + seq_number + ", " + sql_rule_id + ", 0)"
        logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_lt()#prod_name:" + prod_name + \
               "# query 4=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_lt()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 4 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)

    def adding_codeset_all_codes(self, prod_name, benefit_level_name, product_id, product_period,
                                                 benefit_level, conn, seq_number):
        """ ADDING 'Codeset = General Exclusion Codes' RULE FOR 'Coverage Rules' SCREEN -8.3.
        --COVERAGE RULES
        --4.Codeset = All Codes
        Parameters:
            self :Default.
            prod_name :Product name.
            benefit_level_name :Benefit level name.
            product_id : product_id.
            product_period : product_period.
            benefit_level : benefit_level.
            conn : conn.
            seq_number : seq_number.
        Returns: ''
        """
        seq_number = str(seq_number)
        query = "INSERT INTO [EnterpriseDb].[dbo].[SQL_RULES] VALUES (' AND CC.CODESET_ID = 8', ' AND Codeset = All Codes',2)"
        logs = "[CoverageRules:adding_codeset_all_codes()#prod_name:" + prod_name + \
               "#benefit_level_name:" + str(benefit_level_name) + "# query 1=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_codes()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 1 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)



        try:
            sql_rule_id = ''
            query = "SELECT  SCOPE_IDENTITY() sql_rule_id"
            logs = "[CoverageRules:adding_codeset_all_codes()#prod_name:" + prod_name + \
               "# query 2=" + \
               str(query) + " ]"
            PdmLogger.instance().configure_logger().info(logs)
            dfs = pd.read_sql_query(query, conn)
            for index, row in dfs.iterrows():
                sql_rule_id = str(row['sql_rule_id'])
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_codes()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 2 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)


        # DONE
        query = "INSERT INTO [EnterpriseDb].[dbo].[SQL_RULE_DETAIL] VALUES (" + sql_rule_id + ", 2,'=', '8', 'CC.CODESET_ID = 8', 'Codeset = All Codes')"
        logs = "[CoverageRules:adding_codeset_all_codes()#prod_name:" + prod_name + \
               "# query 3=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_codes()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 3 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)


        # ##########################[ VERIFY CHECKBOX IS NEED OR NOT ]################################
        # is_same_copay_coinsurance:different copay or coinsurance
        check_box_needed = '0'
        is_no_benefit_for_oon = str(config.is_no_benefit_for_oon)
        str_copay_insurance = str(config.copay_insurance)
        benefit_level_type_1 = ['In Network', 'Out of Network']
        benefits_pkg_type = str(config.benefit_package_plans)

        if benefits_pkg_type == 'Exam Only' and 'Out of Network' in benefit_level_name \
                and is_no_benefit_for_oon == 'true':
            check_box_needed = '0'
        elif 'EHB Exam Only (Pediatric Only)' in benefits_pkg_type and 'Out of Network' in benefit_level_name \
                and is_no_benefit_for_oon == 'true':
            check_box_needed = '0'
        elif 'Pediatric Low Vision' in benefits_pkg_type and 'Out of Network' in benefit_level_name:
            check_box_needed = '0'
        elif benefits_pkg_type == 'EHB' and 'Out of Network' in benefit_level_name \
                and is_no_benefit_for_oon == 'true':
            check_box_needed = '0'
        elif str(benefit_level_type_1) == str(config.list_of_benefit_level) and 'Out of Network' in benefit_level_name:
            if benefits_pkg_type != 'EHB':
                check_box_needed = '1'
        elif 'Out of Network' in benefit_level_name and str(benefit_level_type_1) != str(config.list_of_benefit_level):
            if benefits_pkg_type != 'EHB':
                check_box_needed = '1'
        # ##########################[ END CHECKBOX CONDITION ]########################################
        query = "INSERT INTO [EnterpriseDb].[dbo].[COVERAGE_RULES] VALUES (" + product_id + "," + product_period + "," + benefit_level + "," + seq_number + ", " + sql_rule_id + ", " + check_box_needed + ")"
        logs = "[CoverageRules:adding_codeset_all_codes()#prod_name:" + prod_name + \
               "#benefits_pkg_type:" + benefits_pkg_type + "#check_box_needed:" + str(check_box_needed) + " query 4=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_codes()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 4 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)


    def adding_codeset_all_low_vision(self, prod_name, benefit_level_name, product_id, product_period,
                                                 benefit_level, conn, seq_number, age_variable):
        """ ADDING COVERAGE RULES FOR 'Coverage Rules' SCREEN -8.3.
        --COVERAGE RULES
        --5.Codeset in (low visionfit,Low vison Materials, Low Vision Testing, Low vision Therapy)AND Member Age < " + age_variable + "
        Parameters:
            self :Default.
            prod_name :Product name.
            benefit_level_name :Benefit level name.
            product_id : product_id.
            product_period : product_period.
            benefit_level : benefit_level.
            conn : conn.
            seq_number : seq_number.
            age_variable : age_variable.
        Returns: ''
        """
        seq_number = str(seq_number)
        query = "INSERT INTO [EnterpriseDb].[dbo].[SQL_RULES] VALUES (' AND CC.CODESET_ID In (59,20,60,61) AND CH.AGE < " + age_variable + "',' AND Codeset In (Low Vision Fit,Low Vision Materials,Low Vision Testing,Low Vision Therapy) AND Member Age < " + age_variable + "',2)"
        logs = "[CoverageRules:adding_codeset_all_low_vision()#prod_name:" + prod_name + \
               "#benefit_level_name:" + str(benefit_level_name) + "# query 1=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_low_vision()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 1 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)



        try:
            sql_rule_id = ''
            query = "SELECT  SCOPE_IDENTITY() sql_rule_id"
            logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_lt()#prod_name:" + prod_name + \
               "# query 2=" + \
               str(query) + " ]"
            PdmLogger.instance().configure_logger().info(logs)
            dfs = pd.read_sql_query(query, conn)
            for index, row in dfs.iterrows():
                sql_rule_id = str(row['sql_rule_id'])
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_codes_and_member_age_lt()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 2 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)


        # DONE
        query = "INSERT INTO [EnterpriseDb].[dbo].[SQL_RULE_DETAIL] VALUES (" + sql_rule_id + ", 2,'In', '(59,20,60,61)', 'CC.CODESET_ID In (59,20,60,61)', 'Codeset In (Low Vision Fit,Low Vision Materials,Low Vision Testing,Low Vision Therapy)'),(" + sql_rule_id + ", 14,'<', '" + age_variable + "', 'CH.AGE < " + age_variable + "', 'Member Age < " + age_variable + "')"
        logs = "[CoverageRules:adding_codeset_all_low_vision()#prod_name:" + prod_name + \
               "# query 3=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_low_vision()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 3 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)

        # ###############[ CHECKBOX SELECTED ]#########################
        query = "INSERT INTO [EnterpriseDb].[dbo].[COVERAGE_RULES] VALUES (" + product_id + "," + product_period + "," + benefit_level + "," + seq_number + ", " + sql_rule_id + ", 1)"
        logs = "[CoverageRules:adding_codeset_all_low_vision()#prod_name:" + prod_name + \
               "# query 4=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_low_vision()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 4 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)


    def adding_codeset_all_materials_contact_lens_fit_and_member_age(self, prod_name, benefit_level_name, product_id,
                                                                     product_period,
                                                                     benefit_level, conn, seq_number, age_variable):
        """ ADDING COVERAGE RULES FOR 'Coverage Rules' SCREEN -8.3.
        --COVERAGE RULES
        ----6.Codeset=All Materials+Contact Lens Fit and Member Age > " + age_variable + "
        Parameters:
            self :Default.
            prod_name :Product name.
            benefit_level_name :Benefit level name.
            product_id : product_id.
            product_period : product_period.
            benefit_level : benefit_level.
            conn : conn.
            seq_number : seq_number.
            age_variable : age_variable.
        Returns: ''
        """
        seq_number = str(seq_number)
        query = "INSERT INTO [EnterpriseDb].[dbo].[SQL_RULES] VALUES (' AND CC.CODESET_ID = 90 AND CH.AGE > " + age_variable + "', ' AND Codeset = All Materials + Contact Lens Fit AND Member Age > " + age_variable + "',2)"
        logs = "[CoverageRules:adding_codeset_all_materials_contact_lens_fit_and_member_age()#prod_name:" + prod_name + \
               "#benefit_level_name:" + str(benefit_level_name) + "# query 1=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_materials_contact_lens_fit_and_member_age()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 1 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)


        try:
            sql_rule_id = ''
            query = "SELECT  SCOPE_IDENTITY() sql_rule_id"
            logs = "[CoverageRules:adding_codeset_all_materials_contact_lens_fit_and_member_age()#prod_name:" + prod_name + \
               "# query 2=" + \
               str(query) + " ]"
            PdmLogger.instance().configure_logger().info(logs)
            dfs = pd.read_sql_query(query, conn)
            for index, row in dfs.iterrows():
                sql_rule_id = str(row['sql_rule_id'])
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_materials_contact_lens_fit_and_member_age()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 2 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)


        # DONE
        query = "INSERT INTO [EnterpriseDb].[dbo].[SQL_RULE_DETAIL] VALUES (" + sql_rule_id + ", 2,'=', '90', 'CC.CODESET_ID = 90', 'Codeset = All Materials + Contact Lens Fit'),(" + sql_rule_id + ", 14,'>', '" + age_variable + "', 'CH.AGE > " + age_variable + "', 'Member Age > " + age_variable + "')"
        logs = "[CoverageRules:adding_codeset_all_materials_contact_lens_fit_and_member_age()#prod_name:" + prod_name + \
               "# query 3=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)

        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_materials_contact_lens_fit_and_member_age()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 3 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)


        query = "INSERT INTO [EnterpriseDb].[dbo].[COVERAGE_RULES] VALUES (" + product_id + "," + product_period + "," + benefit_level + "," + seq_number + ", " + sql_rule_id + ", 0)"
        logs = "[CoverageRules:adding_codeset_all_materials_contact_lens_fit_and_member_age()#prod_name:" + prod_name + \
               "# query 4=" + \
               str(query) + " ]"
        PdmLogger.instance().configure_logger().info(logs)
        try:
            query = str(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as ex:
            logs = "[CoverageRules:adding_codeset_all_materials_contact_lens_fit_and_member_age()#pdm_worker:" + self.pdm_worker \
                   + "#prod_name :" + prod_name + \
                   "#query 4 Exception:" + str(ex) + "]"
            PdmLogger.instance().configure_logger().error(logs)


    def in_network_not_adult_exam_coverage_rules(self, prod_name, benefit_level_name, product_id, product_period,
                                                 benefit_level, conn):
        """ ADDING COVERAGE RULES WHEN IN-NETWORK,NOT ADULT EXAM COVERED FOR 'Coverage Rules' SCREEN -8.3.
        Parameters:
            self :Default.
            prod_name :Product name.
            benefit_level_name :Benefit level name.
            product_id : product_id.
            product_period : product_period.
            benefit_level : benefit_level.
            conn : conn.
        Returns: ''
        """
        dependent_age_limit_info = str(config.dependent_age_limit)
        logs = "[CoverageRules:in_network_not_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker +\
               "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) +\
               "#dependent_age_limit_info:" + dependent_age_limit_info + "#product_id:" + str(product_id) + " ]"
        PdmLogger.instance().configure_logger().info(logs)


        try:
            is_no_benefit_for_oon = str(config.is_no_benefit_for_oon)
            seq_number = 1
            code_set_text = ' Codeset = General Exclusion Codes'
            res = self.adding_codeset_general_exclusion_codes(prod_name, benefit_level_name, product_id, product_period,
                                                        benefit_level, conn, seq_number)
            if(res == 'fail'):
                return 'fail'
            logs = "[CoverageRules:in_network_not_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                   "#adding code_set_text:" + code_set_text + "#is_no_benefit_for_oon:"+ is_no_benefit_for_oon + "]"
            PdmLogger.instance().configure_logger().info(logs)
            if 'Out of Network' in benefit_level_name and is_no_benefit_for_oon == 'true':
                seq_number = 2
                code_set_text = ' Codeset = All Codes'
                res = self.adding_codeset_all_codes(prod_name, benefit_level_name, product_id,
                                              product_period,
                                              benefit_level, conn, seq_number)
                if(res== 'fail'):
                    return 'fail'
                logs = "[CoverageRules:in_network_not_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                       "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                       "#adding code_set_text:" + code_set_text + "#is_no_benefit_for_oon:" + is_no_benefit_for_oon + "]"
                PdmLogger.instance().configure_logger().info(logs)
            else:
                if dependent_age_limit_info == '0-18' \
                        or dependent_age_limit_info == '0-19' \
                        or dependent_age_limit_info == '0-20' \
                        or dependent_age_limit_info == '0-21' \
                        or dependent_age_limit_info == '0-24':
                    print('ok')
                else:
                    logs = "[CoverageRules:in_network_not_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                           "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                           "#NOT ADDED due to not match dependent_age_limit_info:" + dependent_age_limit_info + "]"
                    PdmLogger.instance().configure_logger().error(logs)
                    return 'fail'
                if dependent_age_limit_info == '0-24':
                    age_variable = '24'
                elif dependent_age_limit_info == '0-21':
                    age_variable = '21'
                elif dependent_age_limit_info == '0-20':
                    age_variable = '20'
                elif dependent_age_limit_info == '0-19':
                    age_variable = '19'
                elif dependent_age_limit_info == '0-18':
                    age_variable = '18'
                else:
                    age_variable = '18'
                seq_number = 2
                code_set_text = ' Codeset = All Codes AND Member Age > ' + age_variable
                res = self.adding_codeset_all_codes_and_member_age_gt(prod_name, benefit_level_name, product_id,
                                                                product_period,
                                                                benefit_level, conn, seq_number, age_variable)
                if(res == 'fail'):
                    return 'fail'

        except NoSuchElementException as e:
            print("in_network_not_adult_exam_coverage_rules()#Element Not present ", e)
            logs = "[CoverageRules:in_network_not_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker +\
                   "#prod_name :" + prod_name + "#Element Not present:" + str(e) + "]"
            PdmLogger.instance().configure_logger().error(logs)
            return 'fail'
    pass

    def in_network_not_adult_exam_coverage_rules_member_age(self, prod_name, benefit_level_name, member_age, product_id,
                                                            product_period, benefit_level, conn):
        """ ADDING COVERAGE RULES WHEN IN-NETWORK,NOT ADULT EXAM COVERED FOR 'Coverage Rules' SCREEN -8.3.
        Parameters:
            self :Default.
            prod_name :Product name.
            benefit_level_name :Benefit level name.
            member_age :member_age.
            product_id : product_id.
            product_period : product_period.
            benefit_level : benefit_level.
            conn : conn.
        Returns: ''
        """

        try:
            seq_number = 1
            code_set_text = ' Codeset = General Exclusion Codes'
            self.adding_codeset_general_exclusion_codes(prod_name, benefit_level_name, product_id, product_period,
                                                        benefit_level, conn, seq_number)
            logs = "[CoverageRules:in_network_not_adult_exam_coverage_rules_member_age()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                   "#member_age:" + member_age + "#code_set_text:" + code_set_text + " ]"
            PdmLogger.instance().configure_logger().info(logs)

            seq_number = 2
            code_set_text = ' Codeset = All Codes AND Member Age > ' + member_age
            res = self.adding_codeset_all_codes_and_member_age_gt(prod_name, benefit_level_name, product_id,
                                                            product_period,
                                                            benefit_level, conn, seq_number, member_age)
            if(res == 'fail'):
                return 'fail'
            logs = "[CoverageRules:in_network_not_adult_exam_coverage_rules_member_age()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                   "#member_age:" + member_age + "#code_set_text:" + code_set_text + " ]"
            PdmLogger.instance().configure_logger().info(logs)
        except NoSuchElementException as e:
            print("in_network_not_adult_exam_coverage_rules_member_age()#Element Not present ", e)
            logs = "[CoverageRules:in_network_not_adult_exam_coverage_rules_member_age()#pdm_worker:" + self.pdm_worker +\
                   "#prod_name :" + prod_name + "#Element Not present:" + str(e) + "]"
            PdmLogger.instance().configure_logger().error(logs)
            return 'fail'
            pass
    pass

    def out_of_network_adult_exam_coverage_rules(self, prod_name, benefit_level_name, product_id, product_period,
                                                 benefit_level, conn):
        """ ADDING COVERAGE RULES WHEN OUT-OF-NETWORK,ADULT EXAM FOR 'Coverage Rules' SCREEN -8.4.
        Parameters:
            self :Default.
            prod_name :Product name.
            benefit_level_name :Benefit level name.
            product_id : product_id.
            product_period : product_period.
            benefit_level : benefit_level.
            conn : conn.
        Returns: ''
        """


        dependent_age_limit_info = str(config.dependent_age_limit)
        is_no_benefit_for_oon = str(config.is_no_benefit_for_oon)

        logs = "[CoverageRules:out_of_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
               "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
               "#dependent_age_limit_info:" + dependent_age_limit_info + "]"
        PdmLogger.instance().configure_logger().info(logs)
        if dependent_age_limit_info == '0-18' \
                or dependent_age_limit_info == '0-19' \
                or dependent_age_limit_info == '0-20' \
                or dependent_age_limit_info == '0-21' \
                or dependent_age_limit_info == '0-24':
            print('ok')
        else:
            logs = "[CoverageRules:out_of_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                   "#NOT ADDED due to not match dependent_age_limit_info:" + dependent_age_limit_info + "]"
            PdmLogger.instance().configure_logger().info(logs)
            return 'fail'
        try:

            seq_number = 1
            code_set_text = ' Codeset = General Exclusion Codes'
            res = self.adding_codeset_general_exclusion_codes(prod_name, benefit_level_name, product_id, product_period,
                                                        benefit_level, conn, seq_number)
            if(res == 'fail'):
                return 'fail'

            logs = "[CoverageRules:out_of_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                   "#dependent_age_limit_info:" + dependent_age_limit_info + \
                   "#is_no_benefit_for_oon:" + is_no_benefit_for_oon + "#code_set_text:" + code_set_text + " ]"
            PdmLogger.instance().configure_logger().info(logs)

            if 'Out of Network' in benefit_level_name and is_no_benefit_for_oon == 'true':
                seq_number = 2
                code_set_text = ' Codeset = All Codes'
                res = self.adding_codeset_all_codes(prod_name, benefit_level_name, product_id,
                                              product_period,
                                              benefit_level, conn, seq_number)
                if(res == 'fail'):
                    return 'fail'

                logs = "[CoverageRules:out_of_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                       "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                       "#dependent_age_limit_info:" + dependent_age_limit_info + \
                       "#is_no_benefit_for_oon:" + is_no_benefit_for_oon + "#code_set_text:" + code_set_text + " ]"
                PdmLogger.instance().configure_logger().info(logs)

                # ##########################################[ new change ]##########################################
                age_variable = ''
                if dependent_age_limit_info == '0-21':
                    age_variable = '22'
                elif dependent_age_limit_info == '0-24':
                    age_variable = '25'
                elif dependent_age_limit_info == '0-20':
                    age_variable = '21'
                elif dependent_age_limit_info == '0-19':
                    age_variable = '20'
                elif dependent_age_limit_info == '0-18':
                    age_variable = '19'
                else:
                    logs = "[CoverageRules:out_of_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                           "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                           "#NOT ADDED ,not match dependent_age_limit_info:" + dependent_age_limit_info + "]"
                    PdmLogger.instance().configure_logger().info(logs)
                    return 'fail'
                seq_number = 3
                code_set_text = ' Codeset In (Low Vision Fit,Low Vision Materials,Low Vision Testing,Low Vision Therapy) AND Member Age < ' + age_variable
                res = self.adding_codeset_all_low_vision(prod_name, benefit_level_name, product_id, product_period,
                                                   benefit_level, conn, seq_number, age_variable)
                if (res == 'fail'):
                    return 'fail'

                logs = "[CoverageRules:out_of_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                       "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                       "#dependent_age_limit_info:" + dependent_age_limit_info + \
                       "#is_no_benefit_for_oon:" + is_no_benefit_for_oon + "#code_set_text:" + code_set_text + " ]"
                PdmLogger.instance().configure_logger().info(logs)


            else:
                age_variable = ''
                if dependent_age_limit_info == '0-21':
                    age_variable = '21'
                elif dependent_age_limit_info == '0-24':
                    age_variable = '24'
                elif dependent_age_limit_info == '0-20':
                    age_variable = '20'
                elif dependent_age_limit_info == '0-19':
                    age_variable = '19'
                elif dependent_age_limit_info == '0-18':
                    age_variable = '18'
                else:
                    logs = "[CoverageRules:out_of_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                           "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                           "#NOT ADDED due to not match dependent_age_limit_info:" + dependent_age_limit_info + "]"
                    PdmLogger.instance().configure_logger().info(logs)
                    return 'fail'

                seq_number = 2
                code_set_text = " Codeset = All Materials + Contact Lens Fit AND Member Age > " + age_variable
                res = self.adding_codeset_all_materials_contact_lens_fit_and_member_age(prod_name, benefit_level_name, product_id,
                                              product_period,
                                              benefit_level, conn, seq_number, age_variable)
                if(res == 'fail'):
                    return 'fail'
                logs = "[CoverageRules:out_of_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                       "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                       "#dependent_age_limit_info:" + dependent_age_limit_info + \
                       "#is_no_benefit_for_oon:" + is_no_benefit_for_oon + "#code_set_text:" + code_set_text + " ]"
                PdmLogger.instance().configure_logger().info(logs)

                age_variable = ''
                if dependent_age_limit_info == '0-21':
                    age_variable = '22'
                elif dependent_age_limit_info == '0-24':
                    age_variable = '25'
                elif dependent_age_limit_info == '0-20':
                    age_variable = '21'
                elif dependent_age_limit_info == '0-19':
                    age_variable = '20'
                elif dependent_age_limit_info == '0-18':
                    age_variable = '19'
                else:
                    logs = "[CoverageRules:out_of_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                           "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                           "#NOT ADDED ,not match dependent_age_limit_info:" + dependent_age_limit_info + "]"
                    PdmLogger.instance().configure_logger().info(logs)
                    return 'fail'

                seq_number = 3
                code_set_text = ' Codeset In (Low Vision Fit,Low Vision Materials,Low Vision Testing,Low Vision Therapy) AND Member Age < ' + age_variable
                res = self.adding_codeset_all_low_vision(prod_name, benefit_level_name, product_id, product_period,
                                                   benefit_level, conn, seq_number, age_variable)
                if(res== 'fail'):
                    return 'fail'

                logs = "[CoverageRules:out_of_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                       "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                       "#dependent_age_limit_info:" + dependent_age_limit_info + \
                       "#is_no_benefit_for_oon:" + is_no_benefit_for_oon + "#code_set_text:" + code_set_text + " ]"
                PdmLogger.instance().configure_logger().info(logs)

        except NoSuchElementException as e:
            print("out_of_network_adult_exam_coverage_rules()#Element Not present ", e)
            logs = "[CoverageRules:out_of_network_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker +\
                   "#prod_name :" + prod_name + "#Element Not present:" + str(e) + "]"
            PdmLogger.instance().configure_logger().error(logs)
            return 'fail'
            pass
    pass

    def out_of_network_not_adult_exam_coverage_rules_member_age(self, prod_name, benefit_level_name, member_age,
                                                                product_id, product_period, benefit_level, conn):
        """ ADDING COVERAGE RULES WHEN OUT-OF-NETWORK,ADULT EXAM FOR 'Coverage Rules' SCREEN -8.5.
        Parameters:
            self :Default.
            prod_name :Product name.
            benefit_level_name :Benefit level name.
            member_age :member_age.
            product_id : product_id.
            product_period : product_period.
            benefit_level : benefit_level.
            conn : conn.
        Returns: ''
        """
        is_no_benefit_for_oon = str(config.is_no_benefit_for_oon)

        try:
            seq_number = 1
            code_set_text = ' Codeset = General Exclusion Codes'
            res = self.adding_codeset_general_exclusion_codes(prod_name, benefit_level_name, product_id, product_period,
                                                        benefit_level, conn, seq_number)
            if(res == 'fail'):
                return 'fail'

            logs = "[CoverageRules:out_of_network_not_adult_exam_coverage_rules_member_age()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                   "#member_age:" + member_age + "#is_no_benefit_for_oon:" + is_no_benefit_for_oon +\
                   "#code_set_text:" + code_set_text + " ]"
            PdmLogger.instance().configure_logger().info(logs)

            if is_no_benefit_for_oon == 'false':
                seq_number = 2
                code_set_text = ' Codeset = All Codes AND Member Age > ' + member_age
                res = self.adding_codeset_all_codes_and_member_age_gt(prod_name, benefit_level_name, product_id,
                                                                product_period,
                                                                benefit_level, conn, seq_number, member_age)
                if (res == 'fail'):
                    return 'fail'
                logs = "[CoverageRules:out_of_network_not_adult_exam_coverage_rules_member_age()#pdm_worker:" + self.pdm_worker + \
                       "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                       "#member_age:" + member_age + "#is_no_benefit_for_oon:" + is_no_benefit_for_oon + \
                       "#code_set_text:" + code_set_text + " ]"
                PdmLogger.instance().configure_logger().info(logs)

                age_variable = ''
                if member_age == '18':
                    age_variable = '19'
                elif member_age == '19':
                    age_variable = '20'
                elif member_age == '20':
                    age_variable = '21'
                elif member_age == '21':
                    age_variable = '22'
                elif member_age == '24':
                    age_variable = '25'
                elif member_age == '24':
                    age_variable = '25'
                  
                else:
                    logs = "[CoverageRules:out_of_network_not_adult_exam_coverage_rules_member_age()#pdm_worker:" + self.pdm_worker + \
                           "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                           "#NOT ADDED FOR member_age:" + member_age + "]"
                    PdmLogger.instance().configure_logger().error(logs)
                    return 'fail'
                seq_number = 3
                code_set_text = " Codeset In (Low Vision Fit,Low Vision Materials,Low Vision Testing,Low Vision Therapy) AND Member Age < " + age_variable
                self.adding_codeset_all_low_vision(prod_name, benefit_level_name, product_id, product_period,
                                              benefit_level, conn, seq_number, age_variable)
                logs = "[CoverageRules:out_of_network_not_adult_exam_coverage_rules_member_age()#pdm_worker:" + self.pdm_worker + \
                       "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                       "#member_age:" + member_age + "#is_no_benefit_for_oon:" + is_no_benefit_for_oon + \
                       "#code_set_text:" + code_set_text + " ]"
                PdmLogger.instance().configure_logger().info(logs)
                pass
            else:
                seq_number = 2
                code_set_text = " Codeset = All Codes"
                self.adding_codeset_all_codes(prod_name, benefit_level_name, product_id, product_period,
                                         benefit_level, conn, seq_number)
                logs = "[CoverageRules:out_of_network_not_adult_exam_coverage_rules_member_age()#pdm_worker:" + self.pdm_worker + \
                       "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                       "#member_age:" + member_age + "#is_no_benefit_for_oon:" + is_no_benefit_for_oon + \
                       "#code_set_text:" + code_set_text + " ]"
                PdmLogger.instance().configure_logger().info(logs)

                age_variable = ''
                if member_age == '18':
                    age_variable = '19'
                elif member_age == '19':
                    age_variable = '20'
                elif member_age == '20':
                    age_variable = '21'
                elif member_age == '21':
                    age_variable = '22'
                elif member_age == '24':
                    age_variable = '25'
                else:
                    logs = "[CoverageRules:out_of_network_not_adult_exam_coverage_rules_member_age()#pdm_worker:" + self.pdm_worker + \
                           "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                           "#NOT ADDED due to member_age:" + member_age + "]"
                    PdmLogger.instance().configure_logger().error(logs)
                    return 'fail'
                seq_number = 3
                code_set_text = " Codeset In (Low Vision Fit,Low Vision Materials,Low Vision Testing,Low Vision Therapy) AND Member Age < " + age_variable
                self.adding_codeset_all_low_vision(prod_name, benefit_level_name, product_id, product_period,
                                                   benefit_level, conn, seq_number, age_variable)
                logs = "[CoverageRules:out_of_network_not_adult_exam_coverage_rules_member_age()#pdm_worker:" + self.pdm_worker + \
                       "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                       "#member_age:" + member_age + "#is_no_benefit_for_oon:" + is_no_benefit_for_oon + \
                       "#code_set_text:" + code_set_text + " ]"
                PdmLogger.instance().configure_logger().info(logs)
                pass
        except NoSuchElementException as e:
            print("out_of_network_not_adult_exam_coverage_rules()#Element Not present ", e)
            logs = "[CoverageRules:out_of_network_not_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker +\
                   "#prod_name :" + prod_name + "#Element Not present:" + str(e) + "]"
            PdmLogger.instance().configure_logger().error(logs)
            return 'fail'
            pass
    pass

    def in_network_19_plus_adult_exam_coverage_rules(self, prod_name, benefit_level_name, product_id, product_period, benefit_level, conn):
        """ ADDING COVERAGE RULES WHEN IN-NETWORK (19+),NOT ADULT EXAM FOR 'Coverage Rules' SCREEN -8.6.
        Parameters:
            self :Default.
            prod_name :Product name.
            benefit_level_name :Benefit level name.
            product_id : product_id.
            product_period : product_period.
            benefit_level : benefit_level.
            conn : conn.
        Returns: ''
        """

        logs = "[CoverageRules:in_network_19_plus_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
               "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + "]"
        PdmLogger.instance().configure_logger().info(logs)

        dependent_age_limit_info = str(config.dependent_age_limit)
        if dependent_age_limit_info == '0-18' \
                or dependent_age_limit_info == '0-19' \
                or dependent_age_limit_info == '0-20' \
                or dependent_age_limit_info == '0-21' \
                or dependent_age_limit_info == '0-24':
            print('ok')
        else:
            logs = "[CoverageRules:in_network_19_plus_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                   "#NOT ADDED due to not match dependent_age_limit_info:" + dependent_age_limit_info + "]"
            PdmLogger.instance().configure_logger().error(logs)
            return 'fail'

        try:
            seq_number = 1
            code_set_text = ' Codeset = General Exclusion Codes'
            res = self.adding_codeset_general_exclusion_codes(prod_name, benefit_level_name, product_id, product_period,
                                                        benefit_level, conn, seq_number)
            if(res == 'fail'):
                return 'fail'

            logs = "[CoverageRules:in_network_19_plus_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                   "#dependent_age_limit_info:" + dependent_age_limit_info + "#code_set_text:" + code_set_text + " ]"
            PdmLogger.instance().configure_logger().info(logs)

            age_variable = ''
            if dependent_age_limit_info == '0-21':
                age_variable = '21'
            elif dependent_age_limit_info == '0-24':
                age_variable = '24'
            elif dependent_age_limit_info == '0-20':
                age_variable = '20'
            elif dependent_age_limit_info == '0-19':
                age_variable = '19'
            elif dependent_age_limit_info == '0-18':
                age_variable = '18'
            seq_number = 2
            code_set_text = ' All Materials + Contact Lens Fit AND Member Age > ' + age_variable
            res = self.adding_codeset_all_materials_contact_lens_fit_and_member_age(prod_name, benefit_level_name, product_id,
                                                                              product_period,
                                                                              benefit_level, conn, seq_number,
                                                                              age_variable)
            if (res == 'fail'):
                return 'fail'
            logs = "[CoverageRules:in_network_19_plus_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                   "#dependent_age_limit_info:" + dependent_age_limit_info + "#code_set_text:" + code_set_text + " ]"
            PdmLogger.instance().configure_logger().info(logs)

            age_variable = ''
            if dependent_age_limit_info == '0-21':
                age_variable = '22'
            elif dependent_age_limit_info == '0-24':
                age_variable = '25'
            elif dependent_age_limit_info == '0-20':
                age_variable = '21'
            elif dependent_age_limit_info == '0-19':
                age_variable = '20'
            elif dependent_age_limit_info == '0-18':
                age_variable = '19'
            seq_number = 3
            code_set_text = ' Codeset = All Codes AND Member Age < ' + age_variable
            res = self.adding_codeset_all_codes_and_member_age_lt(prod_name, benefit_level_name, product_id,
                                                            product_period,
                                                            benefit_level, conn, seq_number, age_variable)
            if (res == 'fail'):
                return 'fail'

            logs = "[CoverageRules:in_network_19_plus_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker + \
                   "#prod_name :" + prod_name + "#benefit_level_name:" + str(benefit_level_name) + \
                   "#dependent_age_limit_info:" + dependent_age_limit_info + "#code_set_text:" + code_set_text + " ]"
            PdmLogger.instance().configure_logger().info(logs)
        except NoSuchElementException as e:
            print("in_network_19_plus_adult_exam_coverage_rules()#Element Not present ", e)
            logs = "[CoverageRules:in_network_19_plus_adult_exam_coverage_rules()#pdm_worker:" + self.pdm_worker +\
                   "#prod_name :" + prod_name + "#Element Not present:" + str(e) + "]"
            PdmLogger.instance().configure_logger().error(logs)
            return 'fail'
            pass
    pass

    def uc_page_nav_frm_open_benefit_plan(self, prod_name):
        """ Navigation for SCREEN-2  from first screen 'OPEN BENEFIT PLAN'.
        Parameters:
            self :Default.
            prod_name :Product name.
        Returns: ''
        """
        print("[ SCREEN-2  prod_name :", prod_name, " ]")
        # GO NEXT PAGE SCREEN-2 'Claim Processing Attributes'
        self.driver.find_element_by_xpath("//a[@id='ctl00_MainContent_ucPageNav_btnNext']").click()
    pass


# ####[ main method ]##########


def main():
    """ main method.
    """
    pass


# driver = webdriver.Chrome(executable_path=r"C:\Python36\chromedriver.exe")
driver = None
row = None
pdm_worker = None
# cancel_network_flag = None
coverage_rules = CoverageRules(driver, row, pdm_worker)

if __name__ == '__main__':
    main()
