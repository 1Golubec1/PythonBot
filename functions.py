from config import *
class FUNCTIONS:
    @staticmethod
    def save_info(connect, user_id, per, meaning):
        connect.execute(f"UPDATE {name_bd} SET {per} = \"{meaning}\" WHERE id = {user_id}")
        connect.commit()

    @staticmethod
    def Connect(connect, cursor):
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {name_bd} (id TEXT, state TEXT, commands TEXT, info_file TEXT, name_func TEXT, func TEXT)""")
        connect.commit()

    @staticmethod
    def check_pl(connect, cursor, user_id):
        if cursor.execute(f"SELECT id FROM {name_bd} WHERE id = {user_id} ").fetchone() is None:
            cursor.execute(
                f"INSERT INTO {name_bd} VALUES ({user_id}, '', '[]', '', '', '{str({})}')")
            connect.commit()
            return True
        return False

    @staticmethod
    def get_variable(connect, user_id, per):
        return connect.execute(f"SELECT {per} FROM {name_bd} WHERE id = {user_id}").fetchone()[0]

    @staticmethod
    def conv_dc_str(a):
        if len(a) > 0:
            str_dc = str(list(map(lambda x: str(x[0])+"_"+str(x[1]).replace(",","---"),(list(a.items())))))[1:]
            str_dc = str_dc[:-1]
            return str_dc
        else:
            return str({})

    @staticmethod
    def conv_str_dc(str_dc):
        try:
            list_dc = list(map(lambda x: x.replace("---", ",").split("_"), str_dc.split(",")))
            new_dc = {}
            for i in list_dc:
                new_dc[i[0].replace("\'", "").replace(" ", "")] = i[1]
            return new_dc
        except:
            return {}