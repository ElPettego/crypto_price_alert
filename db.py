import ast

class DB:
    def __init__(self):
        self.file = './alerts/alerts.csv'

    def add_alert(self, alert : dict) -> None:
        with open(self.file, 'a') as f:
            f.write(str(alert) + '\n')    

    def get_alerts(self, chat_id : int = None) -> list:
        with open(self.file, 'r') as f:
            all_alerts = f.readlines()
        all_alerts_obj = []
        if chat_id is None:
            for aler in all_alerts:
                # print(aler)
                al = ast.literal_eval(aler)
                all_alerts_obj.append(al)
            return all_alerts_obj

        for aler in all_alerts:
            # print(aler)
            al = ast.literal_eval(aler)
            if al.get('chat_id') == chat_id:
                all_alerts_obj.append(al)
        return all_alerts_obj

    def delete_alert(self, chat_id : int, open_date : str) -> None:
        alerts = self.get_alerts()
        for ind, aler in enumerate(alerts):
            # print(type(aler))
            if aler.get('chat_id') == chat_id and aler.get('open_date') == open_date:
                index = ind
                break
        
        del alerts[index]

        alerts = [str(d) + '\n' for d in alerts]

        # print(alerts)

        with open(self.file, 'w') as f:
            f.writelines(alerts)

