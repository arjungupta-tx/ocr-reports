from src.SQLdb.sql_query_engine import fetch_one




def userloging(username:str,password:str):

    try:
        query = f"""
                   select Id_User,Permission,IsActive,Email,Role from User_Table where Email ='{username}' and Password = '{password}'


                 """
        
        result = fetch_one(query)

        return result

    except Exception as e:  
        raise e  
        

