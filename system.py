import random, csv, os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

class Appliance:
    def __init__(self,name,power_watts):
        self.name, self.power_watts=name, power_watts
    def calculate_kwh(self, hours):
        return (self.power_watts * hours) / 1000.0
class User:
    def __init__(self,userID,name):
        self.userID,self.name=userID,name
        self.appliances, self.dailyUsage_record,self.monthly_bill=set(), [], 0.0

class SystemInfo:
    def __init__(self):
        for folder in ("data", "reports", "visualizations"):
               os.makedirs(folder, exist_ok=True)
        self.users,self.appliances={},{}
        self.normal_rate, self.peak_rate, self.overloadLimit = 15.0, 25.0, 50.0
        for name, power in [("Ceiling fan", 75), ("Air conditioner", 1500), ("Refrigerator", 150),
                           ("TV", 100), ("Computer", 200), ("Washing machine", 500),
                           ("Microwave oven", 1200), ("Electric Kettle", 1500), 
                           ("Iron", 1000), ("Vacuum Cleaner", 1400)]:
            self.appliances[name]= Appliance(name, power)

def add_user(sys,uid,name):
    if uid in sys.users: return print(f"Error: User ID {uid} already exists!")
    sys.users[uid] =User(uid,name)
    print(f"User '{name}' added with ID: {uid}")

def remove_user(sys,uid):
    if uid not in sys.users: return print(f"Error: User ID {uid} not found")
    print(f"User '{sys.users[uid].name}' removed")
    del sys.users[uid]

def show_summary(sys,uid):
    if uid not in sys.users: return print(f"Error: User ID {uid} not found")
    u=sys.users[uid]
    print(f"\nUSER SUMMARY - {u.name}\n{'-'*60}")
    print(f"User ID: {uid},Appliances: {len(u.appliances)}")
    if u.appliances: print(f"List: {', '.join(u.appliances)}")
    print(f"Usage Records:{len(u.dailyUsage_record)}")
    if u.dailyUsage_record: print(f"Total kWh: {sum(r[3] for r in u.dailyUsage_record):.2f}")
    if u.monthly_bill>0: print(f"Monthly Bill: Rs. {u.monthly_bill:.2f}")
    print(f"{'-'*60}")

def assign_appliance(sys,uid,app_name):
    if uid not in sys.users: return print(f"Error: User ID {uid} not found")
    if app_name not in sys.appliances: return print(f"Error: Appliance '{app_name}' not found")
    sys.users[uid].appliances.add(app_name)
    print(f"Appliance '{app_name}' assigned to user {uid}")

def simulate_usage(sys,uid,days=30,auto=False):
    if uid not in sys.users: return print(f"Error: User ID {uid} not found")
    u=sys.users[uid]
    if not u.appliances: return print(f"Error: No appliances assigned")

    print(f"\nSimulating {days} days for {u.name}\n")
    u.dailyUsage_record =[]

    for day in range(1, days+1):
        print(f"\nDay {day}")
        daily_total=0.0
        for app_name in u.appliances:
            app=sys.appliances[app_name]
            if auto:
                hrs = 24.0 if app_name == "Refrigerator" else round(random.uniform(0.5, 8), 1)
                print(f"  {app_name}: {hrs}")
            else:
                while True:
                    try:
                        hrs=float(input(f"  {app_name}: "))
                        if 0<=hrs<=24: break
                        print(" Enter 0-24")
                    except: print(" Enter valid number")
            kwh=app.calculate_kwh(hrs)
            u.dailyUsage_record.append([day, app_name, round(hrs, 2), round(kwh, 3), random.random()<0.3])
            daily_total += kwh

        print(f"{'WARNING! HIGH USAGE!' if daily_total>sys.overloadLimit else 'Daily total:'} {daily_total:.2f} kWh")
    print(f"\nSimulation complete")
    save_usage_logs(sys,uid)

def calculate_bill(sys,uid):
    if uid not in sys.users: return print(f"Error: User ID {uid} not found")
    u=sys.users[uid]
    if not u.dailyUsage_record: return print(f"Error: No usage data")
    
    normal_kwh=sum(r[3] for r in u.dailyUsage_record if not r[4])
    peak_kwh =sum(r[3] for r in u.dailyUsage_record if r[4])
    normal_amt,peak_amt =normal_kwh * sys.normal_rate, peak_kwh * sys.peak_rate
    u.monthly_bill = normal_amt+peak_amt

    print(f"\nMONTHLY BILL FOR {u.name} (ID: {uid})\n{'-'*60}")
    print(f"Normal: {normal_kwh:.2f} kWh @ Rs. {sys.normal_rate}/kWh = Rs. {normal_amt:.2f}")
    print(f"Peak: {peak_kwh:.2f} kWh @ Rs. {sys.peak_rate}/kWh = Rs. {peak_amt:.2f}")
    print(f"{'-'*60}\nTOTAL: Rs. {u.monthly_bill:.2f}\n{'-'*60}")
    save_bill(sys,uid,normal_kwh,peak_kwh, u.monthly_bill)

def set_rates(sys,normal=None,peak=None):
    if normal is not None:
        if normal<0: return print("Error: Rate cannot be negative")
        sys.normal_rate=float(normal)
        print(f"Normal rate set to Rs. {normal}/kWh")
    if peak is not None:
        if peak<0: return print("Error: Rate cannot be negative")
        sys.peak_rate=float(peak)
        print(f"Peak rate set to Rs. {peak}/kWh")

def save_usage_logs(sys,uid):
    try:
        u= sys.users[uid]
        with open(f"data/usage_log_{uid}_{u.name.replace(' ', '_')}.csv", 'w', newline='') as f:
            w= csv.writer(f)
            w.writerow(['Day','Appliance','Hours','kWh','Peak'])
            w.writerows(u.dailyUsage_record)
        print(f"Usage logs saved")
    except Exception as e: print(f"Error: {e}")

def save_bill(sys,uid,nkwh,pkwh, total):
    try:
        u =sys.users[uid]
        with open(f"reports/bill_{uid}_{u.name.replace(' ', '_')}.csv", 'w', newline='') as f:
            w=csv.writer(f)
            w.writerows([['Bill Summary for', u.name], ['User ID', uid], [],
                        ['Description', 'kWh', 'Rate', 'Amount'],
                        ['Normal', f'{nkwh:.2f}', f'{sys.normal_rate:.2f}', f'{nkwh*sys.normal_rate:.2f}'],
                        ['Peak', f'{pkwh:.2f}', f'{sys.peak_rate:.2f}', f'{pkwh*sys.peak_rate:.2f}'],
                        [], ['TOTAL', '', '', f'{total:.2f}']])
        print(f"Bill saved")
    except Exception as e: print(f"Error: {e}")

def generate_report(sys):
    try:
        if not sys.users: return print("No users in system")
        with open("reports/complete_report.csv", 'w', newline='') as f:
            w =csv.writer(f)
            w.writerow(['User ID', 'Name', 'Appliances', 'Total kWh', 'Bill (Rs)'])
            for uid, u in sys.users.items():
                w.writerow([uid,u.name,len(u.appliances),
                           f'{sum(r[3] for r in u.dailyUsage_record):.2f}', f'{u.monthly_bill:.2f}'])
        print("Complete report saved")
    except Exception as e: print(f"Error: {e}")

def viz_appliance(sys, uid):
    if uid not in sys.users or not sys.users[uid].dailyUsage_record: return print("Error: No data")
    u=sys.users[uid]
    ac={}
    for r in u.dailyUsage_record: ac[r[1]]= ac.get(r[1], 0) + r[3]
    
    plt.figure(figsize=(12, 6))
    bars=plt.bar(ac.keys(), ac.values(), color='blue', edgecolor='black')
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.,h,f'{h:.2f}',ha='center',va='bottom')
    plt.xlabel('Appliances', fontweight='bold')
    plt.ylabel('Energy (kWh)', fontweight='bold')
    plt.title(f'Monthly Consumption - {u.name}', fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"visualizations/appliance_{uid}.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Chart saved")

def viz_trend(sys,uid):
    if uid not in sys.users or not sys.users[uid].dailyUsage_record: return print("Error: No data")
    u=sys.users[uid]
    dt={}
    for r in u.dailyUsage_record: dt[r[0]]=dt.get(r[0], 0) + r[3]
    days=sorted(dt.keys())
    cons=[dt[d] for d in days]
    avg=sum(cons) / len(cons)
    
    plt.figure(figsize=(14,6))
    plt.plot(days, cons, marker='o', linewidth=2, color='darkgreen')
    plt.axhline(y=avg, color='red', linestyle='--', label=f'Avg: {avg:.2f} kWh')
    plt.xlabel('Day', fontweight='bold')
    plt.ylabel('Energy (kWh)', fontweight='bold')
    plt.title(f'Daily Trend - {u.name}', fontweight='bold')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"visualizations/trend_{uid}.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Chart saved")

def viz_peak_normal(sys, uid):
    if uid not in sys.users or not sys.users[uid].dailyUsage_record: return print("Error: No data")
    u=sys.users[uid]
    dd={}
    for r in u.dailyUsage_record:
        if r[0] not in dd: dd[r[0]] = {'peak': 0.0, 'normal': 0.0}
        dd[r[0]]['peak' if r[4] else 'normal'] += r[3]
    
    days=sorted(dd.keys())
    peak=[dd[d]['peak'] for d in days]
    normal=[dd[d]['normal'] for d in days]
    
    plt.figure(figsize=(14, 6))
    plt.bar(days,normal,label='Normal', color='lightblue', edgecolor='black')
    plt.bar(days,peak,bottom=normal, label='Peak', color='orange', edgecolor='black')
    plt.xlabel('Day', fontweight='bold')
    plt.ylabel('Energy (kWh)', fontweight='bold')
    plt.title(f'Peak vs Normal - {u.name}', fontweight='bold')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"visualizations/peak_normal_{uid}.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Chart saved")

def predict_next(sys, uid):
    if uid not in sys.users or not sys.users[uid].dailyUsage_record: return print("Error: No data")
    u=sys.users[uid]
    dt={}
    for r in u.dailyUsage_record: dt[r[0]] = dt.get(r[0], 0) + r[3]
    days=sorted(dt.keys())
    cons=[dt[d] for d in days]
    
    X=np.array(days).reshape(-1, 1)
    y=np.array(cons)
    model = LinearRegression().fit(X, y)
    
    last = max(days)
    future =np.array(range(last +1,last+31)).reshape(-1, 1)
    pred=np.maximum(model.predict(future), 0)
    
    peak_ratio=sum(1 for r in u.dailyUsage_record if r[4])/len(u.dailyUsage_record)
    total_pred=sum(pred)
    pred_peak=total_pred*peak_ratio
    pred_normal=total_pred*(1 - peak_ratio)
    pred_bill=pred_normal*sys.normal_rate+pred_peak*sys.peak_rate
    
    print(f"\nPREDICTION FOR {u.name}\n{'-'*60}")
    print(f"Current month: {sum(y):.2f} kWh")
    print(f"Predicted next: {total_pred:.2f} kWh")
    print(f"Predicted bill: Rs. {pred_bill:.2f}")
    
    plt.figure(figsize=(14, 6))
    plt.scatter(X, y, color='blue',label='Current',s=50, alpha=0.6)
    plt.plot(X, y, color='blue', alpha=0.3)
    plt.scatter(future, pred, color='red', label='Predicted', s=50, alpha=0.6)
    plt.plot(future, pred, color='red', alpha=0.3)
    all_X = np.concatenate([X, future])
    plt.plot(all_X, model.predict(all_X), 'g--', linewidth=2, label='Trend')
    plt.xlabel('Day', fontweight='bold')
    plt.ylabel('Consumption (kWh)',fontweight='bold')
    plt.title(f'Prediction - {u.name}', fontweight='bold')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"visualizations/prediction_{uid}.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Prediction chart saved")
