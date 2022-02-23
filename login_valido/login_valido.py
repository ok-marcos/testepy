import os
from sys import argv
from operator import add
from functools import reduce
import requests
import json
from faker import Faker


def digit_calc(partial_num):
    p_cpf = list(partial_num)
    V_AUX1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    V_AUX2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    v_res1 = []
    v_res2 = []
    # Calculo do primeiro digito verificador
    [v_res1.append(int(k) * i) for k, i in zip(p_cpf, V_AUX1)]
    p_dig1 = reduce(add, v_res1) % 11
    if p_dig1 > 1:
        dig_1 = 11 - p_dig1
    else:
        dig_1 = 0
    p_cpf.append(str(dig_1))
    # Calculo do segundo digito verificador
    [v_res2.append(int(k) * i) for k, i in zip(p_cpf, V_AUX2)]
    p_dig2 = reduce(add, v_res2) % 11
    if p_dig2 > 1:
        dig_2 = 11 - p_dig2
    else:
        dig_2 = 0
    p_cpf.append(str(dig_2))
    return ''.join(p_cpf)


def save_file(the_list, file):
    with open(file, 'w') as file_handler:
        for item in the_list:
            file_handler.write("{}\n".format(item))

dict_all = list()
if __name__ == '__main__':
    fake = Faker('pt-BR')
    if len(argv) < 3:
        print('- Digite a quantidade de cpf\'s/email\'s a serem gerados.')
        print('- Digite um nome para o arquivo de saida.')
    else:
        try:
            const_num = fake.random_int(min=100, max=999)
            var_num = [str(const_num) + '{0:06}'.format(k)
                       for k in range(int(argv[1]))]
            cpf_email = []
            for k in var_num:
                cpf = digit_calc(k)
                cpf_mask = '{0}.{1}.{2}-{3}'.format(
                    cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])
                email = '{0}{1}@{2}'.format('qa_perf',
                                            cpf, 'performancelivelo.com.br')
                CLM_connection = requests.get(
                    "https://auth-uat.pontoslivelo.com.br/livelo-login/register")
                username = {'username': cpf}
                CLM_connection_cpf = requests.post(
                    'https://auth-uat.pontoslivelo.com.br/livelo-login/send-to-register', data=username)
                head = {
                    'Connection': 'keep-alive',
                    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json; charset=UTF-8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
                    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
                    'Content-Length': '329',
                    'Host': 'auth-uat.pontoslivelo.com.br'
                }
                name = fake.name()
                gender = fake.random.choice(['F', 'M'])
                data = {
                    "userId": cpf,
                    "fullName": name,
                    "gender": gender,
                    "birthDate": "1983-05-14",
                    "cellPhone": "11922222222",
                    "email": email,
                    "sendEmail": False,
                    "sendSms": False,
                    "sendPush": False,
                    "sendWpp": False,
                    "sendPromo": False,
                    "sendEduc": False
                }
                teste = json.dumps(data)
                CLM_connection_user = requests.put(
                    'https://auth-uat.pontoslivelo.com.br/livelo-login/tracking', headers=head, data=teste)
                password = fake.random_int(min=100000, max=999999)
                CLM_connection_password = requests.post(
                    "https://auth-uat.pontoslivelo.com.br/livelo-login/doRegister?g-recaptcha-response=&password={password}&gender={gender}&cellphone=%2811%29+92222-2222&confirmPassword={password}&fullName={username}&sessionVariableRecaptcha=true&birthDate=14%2F05%2F1983&email={email}&termsAndConditions=on&username={username}")
                # cpf_email.append('{0};{1};{2};{3};{4};{5}'.format(
                #     cpf, email, cpf_mask, name, gender, password))
                # cpf_dict = dict()

                

                cpf_dict = {'cpf': cpf,
                    'email': email,
                    'cpf_mask': cpf_mask,
                    'name': name,
                    'gender':gender,
                    'password':password
                }

                # dict_all.append(cpf_dict)
                
                # cpf_email.append("'cpf':{0},'email':{1},'cpf_mask':{2},'name':{3},'gender':{4},'password':{5}".format(
                #     cpf, email, cpf_mask, name, gender, password))
            file = '{}/{}.json'.format(os.getcwd(), argv[2])
            # save_file(cpf_dict, file)
            # final_dict = json.dumps(dict_all)
            final_dict = json.dumps(cpf_dict)
            with open(file, 'w') as outfile:
                outfile.write(final_dict)
        except Exception as e:
            print(e)
# python create_data_CLM.py 2 email-users.csv