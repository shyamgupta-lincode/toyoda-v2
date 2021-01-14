from common.utils import MongoHelper
from livis.settings import *
from bson import ObjectId
from plan.utils import get_todays_planned_production_util
from common.utils import GetLabelData
import datetime
from xlsxwriter import Workbook
#######################################################################PART CRUDS#######################################################

def add_logs_util(user_id,operation_type,notes):
    try:
        createdAt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        mp = MongoHelper().getCollection(LOGS_COLLECTION)
        obj = {
            'user_id' : user_id,
            'operation_type' : operation_type,
            "notes" : notes,
            'created_at' : createdAt,
        }
        _id = mp.insert(obj)   
        # print("insert id:::",_id)
        return _id
    except Exception as e:
        return "Could not add log: "+str(e)


def get_access_log_report_util(data):

    #skip = 0
    #limit = 10
    
    from_date = data.get('from_date',None)
    to_date = data.get('to_date',None)
    operator_name = data.get('operator_name',None)
    
    current  = None
    limit_to = None

    try:
        current = data.get('current',None)
    except:
        pass
    try:
        limit_to = data.get('limit',None)
    except:
        pass

    if current is not None:
        current = int(current)
    if limit_to is not None:
        limit_to = int(limit_to)
        
        
    query = []
    
    

    mp = MongoHelper().getCollection(LOGS_COLLECTION)
    
    
    #for skip and limit 
    
    if current is None and limit_to is None:
        p = [i for i in mp.find().sort( "$natural", -1 )]
    
    else:
        
        if current == 1:
            p = [i for i in mp.find().skip(0).limit(limit_to).sort( "$natural", -1 )]
        else:
            skip_from = ((current * limit_to)-limit_to)
            p = [i for i in mp.find().skip(skip_from).limit(limit_to).sort( "$natural", -1 )]
            
            
    #for filter option
    pr = []
    
    def intersection(lst1, lst2): 
        lst3 = [value for value in lst1 if value in lst2] 
        return lst3
    
    if operator_name is not None :
        pr = [i for i in mp.find({'user_id': operator_name}).sort( "$natural", -1 )]
    else :
        pr = [i for i in mp.find().sort( "$natural", -1 )]

    if from_date is not None and to_date is not None :
        pr = [i for i in mp.find(({'created_at': {"$gte":from_date,"$lte":to_date}})).sort( "$natural", -1 )]

    # resp = [p for p in mp.find({"$and" : query}).skip(skip).limit(limit)]

    q = [i for i in mp.find().sort( "$natural", -1 )]
    
    total = len(q)
    
    
    print(pr)
    
    new_lst = intersection(p,pr)
    
    
    message = new_lst
    status_code = 200
    
    
    
    #log_list = []
    #resp = mp.find({}).skip(skip).limit(limit)
    # print("query id:::",resp)
    #if resp:
    #    for log in resp:
            # print(log)
    #        log_list.append(log)
    #total = mp.find({}).count()
    #logs_info = [{"data":log_list,"total":total}]
    # objs =  mp.find(
    #         {
    #             "$and": query
    #         }
    #         )    
    # print("query id:::",objs)
    
    return total,current,limit_to,message,status_code
    #return logs_info
    
def export_logs_list(data):

    try:
        from_date = data['from_date']
    except:
        from_date = None

    try:
        to_date = data['to_date']
    except:
        to_date = None
        
    try:
        operator_name = data['operator_name']
    except:
        operator_name = None  
        
        
    resp_list = []
    query_1 = []
    
    if from_date is not None and to_date is not None :
        query_1.append({'created_at': {"$gte":from_date,"$lte":to_date}})
        
    if operator_name is not None :
        query_1.append({'user_id': operator_name})
    
    
    mp = MongoHelper().getCollection(LOGS_COLLECTION)
    
    if bool(query_1):
        pr_ids = [i['_id'] for i in mp.find({"$and":query_1})]
        #print("pr_ids")
        #print(pr_ids)
    else:
        pr_ids = [i['_id'] for i in mp.find()]
        
        

    for ind , pr_id in enumerate(pr_ids):
        res = mp.find({"_id":pr_id})
        #print(pr_id)
        #print(res)
        for r in res:
        
            resp_list.append({"id":ind,
                    "user_id": r["user_id"],
                    'operation_type': r['operation_type'] ,
                    'notes':r["notes"],
                    "created_at":r["created_at"]})
                    
    
                   
    return resp_list


def write_excel(list_dict, file_name):
    ordered_list=list(list_dict[0].keys())
    pth = TRAIN_DATA_STATIC + '/' + file_name + ".xlsx"
    wb=Workbook(pth)
    ws=wb.add_worksheet("New Sheet") #or leave it blank, default name is "Sheet 1"
    first_row=0
    for header in ordered_list:
        col=ordered_list.index(header) 
        ws.write(first_row,col,header) 
    row=1
    for dic in list_dict:
#         print(dic)
#         print(dic.items())
        for _key,_value in dic.items():
            col=ordered_list.index(_key)
            ws.write(row,col,_value)
        row+=1 #enter the next row
    wb.close()
    return file_name + '.xlsx'
    
    
def export_file(list_dict,file_name):
    fn = write_excel(list_dict, file_name)
    return "http://127.0.0.1:3306/"+fn

def export_logs_util(data):

    list_dict = export_logs_list(data)
    #file_name = os.path.join(path,"report_details")
    file_name = "log_report_details"
    fn = export_file(list_dict,file_name)
    return fn,200
    
        
    

    
    
    

