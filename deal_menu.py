import uuid

def single_deal(eid, module_id):
    id =  str(uuid.uuid4()).replace('-', '')
    sql_template = f"insert ignore into enterprise_module_master_mapping_new(id, enterprise_id, module_id, order_id) values ('{id}', '{eid}', '{module_id}', 2);\n"
    return sql_template
    
def batch_deal(eids):
    sql_content = ""
    eidList = eids.split(',')
    module_id = '856363557683974704'
    for eid in eidList:
       sql_content += single_deal(eid)
    return sql_content
       
       
if __name__ == "__main__":

    eids = open("C:\\Users\\syske\\Desktop\\eids_version.txt").readlines()
    sql_content = ""
    module_id = '856363557683974704'
    for eid in eids:
        eid = eid.replace("\n", '')
        print(eid)
        sql_content += single_deal(eid, module_id)
    print(sql_content)
    open("version_update.sql", mode='w+').write(sql_content)