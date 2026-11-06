import pandas as pd

class LunarGlassFactory:
    def __init__(self):
        # 1. المدخلات (التربة القمرية من مصنع الماء)
        self.daily_regolith_kg = 2000       # كمية التربة الجافة المتاحة يومياً (كغ)
        self.glass_yield_percentage = 0.40  # نسبة التربة التي تتحول إلى زجاج (40%)
        self.block_yield_percentage = 0.50  # نسبة التربة التي تتحول إلى بلوك بناء (50%)
        self.metal_yield_percentage = 0.10  # نسبة المعادن المستخرجة (10%)
        
        # 2. متغيرات الطاقة (شمسية مركزة)
        self.energy_per_kg_glass_MJ = 2.5   # ميجا جول لصهر 1 كغ زجاج
        self.energy_per_kg_block_MJ = 1.0   # ميجا جول لصهر 1 كغ بلوك
        self.solar_efficiency = 0.85        # كفاءة المرايا الشمسية
        
        # 3. التكاليف (بملايين الدولارات)
        self.capex_plant = 25.0             # تكلفة بناء المصنع (مرايا، أفران، قوالب)
        self.capex_launch = 10.0            # إطلاق المعدات
        self.opex_annual = 0.0              # تكلفة التشغيل (شمس وجاذبية = صفر)
        
        # 4. أسعار الأرض (للمقارنة)
        self.earth_glass_cost_per_kg = 100  # دولار (تكلفة جلب زجاج من الأرض)
        self.earth_block_cost_per_kg = 50   # دولار (تكلفة جلب بلوك من الأرض)

    def calculate_production(self):
        # الإنتاج اليومي
        daily_glass = self.daily_regolith_kg * self.glass_yield_percentage
        daily_blocks = self.daily_regolith_kg * self.block_yield_percentage
        daily_metals = self.daily_regolith_kg * self.metal_yield_percentage
        
        # الإنتاج السنوي (360 يوم عمل)
        annual_glass = daily_glass * 360
        annual_blocks = daily_blocks * 360
        annual_metals = daily_metals * 360
        
        # الطاقة المطلوبة يومياً (ميجا جول)
        daily_energy_glass = daily_glass * self.energy_per_kg_glass_MJ
        daily_energy_blocks = daily_blocks * self.energy_per_kg_block_MJ
        total_daily_energy = (daily_energy_glass + daily_energy_blocks) / self.solar_efficiency
        
        return {
            "daily_glass_kg": daily_glass,
            "daily_blocks_kg": daily_blocks,
            "daily_metals_kg": daily_metals,
            "annual_glass_tons": annual_glass / 1000,
            "annual_blocks_tons": annual_blocks / 1000,
            "annual_metals_tons": annual_metals / 1000,
            "daily_energy_MJ": total_daily_energy
        }

    def calculate_economics(self, years):
        prod = self.calculate_production()
        
        # تكلفة المصنع الإجمالية
        total_capex = self.capex_plant + self.capex_launch
        total_cost = total_capex + (self.opex_annual * years)
        
        # قيمة المنتجات لو جلبناها من الأرض
        earth_cost_glass = (prod["annual_glass_tons"] * 1000) * self.earth_glass_cost_per_kg * years
        earth_cost_blocks = (prod["annual_blocks_tons"] * 1000) * self.earth_block_cost_per_kg * years
        total_earth_cost = (earth_cost_glass + earth_cost_blocks) / 1_000_000 # تحويل إلى مليون دولار
        
        # تكلفة الكيلوغرام الواحد من مصنعنا
        total_kg_produced = (prod["annual_glass_tons"] + prod["annual_blocks_tons"]) * 1000 * years
        isru_cost_per_kg = (total_cost * 1_000_000) / total_kg_produced
        
        return {
            "Years": years,
            "Annual_Glass_Tons": prod["annual_glass_tons"],
            "Annual_Blocks_Tons": prod["annual_blocks_tons"],
            "Total_Cost_M$": total_cost,
            "Earth_Cost_M$": total_earth_cost,
            "ISRU_Cost_per_kg_$": isru_cost_per_kg,
            "Savings_M$": total_earth_cost - total_cost
        }

# --- تشغيل المحاكاة ---
factory = LunarGlassFactory()
prod_data = factory.calculate_production()

print("=== بيانات الإنتاج اليومي والسنوي (مصنع الزجاج والبناء) ===")
print(f"إنتاج الزجاج السنوي: {prod_data['annual_glass_tons']:,.1f} طن")
print(f"إنتاج البلوك السنوي: {prod_data['annual_blocks_tons']:,.1f} طن")
print(f"إنتاج المعادن السنوي: {prod_data['annual_metals_tons']:,.1f} طن")
print(f"الطاقة الشمسية المطلوبة يومياً: {prod_data['daily_energy_MJ']:,.1f} ميجا جول\n")

print("=== الجدول الاقتصادي على مدار 5 سنوات ===")
results = []
for y in [1, 2, 3, 5]:
    results.append(factory.calculate_economics(y))

df = pd.DataFrame(results)
print(df.to_string(index=False))
