import re 

class ScanData:
#
    def __init__(self, content):
        self.content = content
        split_content = re.findall(r'\[FROM_UNIXTIME\(logtime\)\][^()]*', content)
        self.all_data = [self.script(i) for i in split_content]

# output all sorted names of points of all shops > list
    def get_all_points(self):
        return sorted(list(set([x['id'] for x in self.all_data])))

# output one named point with data for any time > list
    def get_point(self, point):
        return [x for x in self.all_data if x['id'] == point]

# output dict {main_name: [all_subname]}
    def get_named_points(self):
        # remove all numeric names
        named_filter = [x for x in self.get_all_points() if any(map(lambda i: i.isalpha(), x))]
        unnamed_filter = [x for x in self.get_all_points() if all(map(lambda i: not i.isalpha(), x)) and x]

        # split name with last '_' to list MAIN_name
        shops_list = sorted(list(set([x[:x.rfind('_')] for x in named_filter if '_' in x])))
        shops_dict = {}
        shops_dict['_UNNAMED'] = sorted(unnamed_filter)
        for x in shops_list:
           shops_dict[x] = sorted(list(set([i['id'] for i in self.all_data if x in i['id']])))
        return shops_dict

# output string with sensors info
    def sensor_info(self, data):
        sensor_time = data['time']
        sensor_values = data['data']
        values_text = [f'{sensor_time}  ID_sensor: {x.get("ID_sensor", "")} -- temp: {x.get("temp", "")}' for x in sensor_values if sensor_values]
        return values_text

# temporary script for inside things
    def script(self, i):
        i = i.replace('\\', '')
        bin = {}
        bin['time'] = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', i)[0]
        bin['ip'] = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', i)[0]
        if '"id":' in i:
            bin['id'] = re.findall(r'"id":"([^\"]*)"', i.replace(' ',''))[0]
        else:
            bin['id'] = ''
        if '"sensor_data":' in i:
            bin['data'] = eval(re.findall(r'"sensor_data":(\[[^\]]*\])', i.replace(' ','').replace('null', 'None'))[0])
        else:
            bin['data'] = ''
        return bin

