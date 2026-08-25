#!/usr/bin/env python3
"""Whisper 并发转录管理器：保持 CONCURRENCY 并发，跳过已完成。"""
import subprocess, time
from pathlib import Path

ROOT = Path.cwd()
FILES = [
    'jundongkou_communication_ep250.m4a',
    '3t_mountain_horror_vol99.m4a',
    'ep027_worldcup_fifa_power.m4a',
    'carb_science_e16.m4a',
    'sichuan_people_ep107.m4a',
    'pingyang_vienna_escape.m4a',
    'yangtianzhen_growth_ep007.m4a',
    'peter_marlow_magnum29.m4a',
    'japan_elderly_life_ep44.m4a',
    'summer_camera_2026_ai.m4a',
    'disney_express_pass_ep023.m4a',
    'spain_argentina_football.m4a',
    'gudian_antineihao_ep11.m4a',
    'tiwei_management_weimei.m4a',
    'nepal_act_hiking_guide.m4a',
    'outdoor_gear_gender_guide.m4a',
    'huanxingdi_rome_resist.m4a',
    'xiazheng_tea_market_9q.m4a',
    'gudian_commute_ep3.m4a',
    'rights_protection_ep231.m4a',
    'wenhua_summer339.m4a',
    'sisreads_girl_grow_summer.m4a',
    'weixiaokang_ai_org.m4a',
    'sisreads_graduation_society.m4a',
    'ziran_fat_loss_vol65.m4a',
    'ai_model_problem_first.m4a',
    'us_tipping_invisible_tax.m4a',
    'sams_china_exec_us_soccer.m4a',
    'ep199_future_life_guide.m4a',
    'greatwall_mpv_suv_naming.m4a',
    'feipian_photography.m4a',
    '2ndstreet_japan_used_clothing.m4a',
    'doubao_pro_football_jersey.m4a',
    'dongpeng_rtd_coffee_share.m4a',
    'shanshen_jingshan_qingshan.m4a',
    'shenzhen_survival_manual.m4a',
    'shenzhen_survival_manual_ep185.m4a',
    'diqi_chedai_zhenxiang.m4a',
    'polyglot_five_languages.m4a',
    'us_medical_ai_market.m4a',
    'uniqlo_aesthetic_spotlight.m4a',
    'malaysia_7day_travel_guide.m4a',
    'product_qiuzhi_resume_talk.m4a',
    'ai_app_burst_e223.m4a',
    'quanji_hotel_oriental_aesthetics.m4a',
    'saas_ai_org_reform_e225.m4a',
    'google_tpu_nvidia_e228.m4a',
    'ikea_stockholm2025.m4a',
    'xpeng_v2_vla.m4a',
    'jia_huihua_tizhinei.m4a',
    'zhangxue_jinianbaohong.m4a',
    'gangrenboqi_zhuanshan_guide.m4a',
    'thinking_fast_slow_brain.m4a',
    'fatigue_economics_e227.m4a',
    'zhangxiaoyu_life_serious.m4a',
    'yaoshunyu_ai_interview.m4a',
    'outdoor_geography_class.m4a',
    'model_y_3year_loss_champion.m4a',
    'beijing_autoshow_beyond_cars.m4a',
    'lidar_800v_ideal_l9.m4a',
    'buy_car_impulse_guide.m4a',
    'greenlights_v329.m4a',
    'tesla_xinwangda_battery.m4a',
    'work_value_rebuild.m4a',
    'ev_battery_lock_ota.m4a',
    'li_l9_livis_emotion_value.m4a',
    'deepseek_v4_infra_context.m4a',
    'iiac_coffee_gold_award.m4a',
    'smart_perception_sensors.m4a',
    'worldcup_2026_guide.m4a',
    'liuzhenyun_ep01_dialogue.m4a',
    'jlr_maserati_huawei_ev.m4a',
    'zhineng_yanjing_xuanpin_guide.m4a',
    'photography_self_learn.m4a',
    'camera_phone_lazy_debate.m4a',
    'clawdbot_2026_phenomenon.m4a',
    'ningshi_shenyuan_overseas_case.m4a',
    'labubu_chaowan_legacy.m4a',
    'huanqiu_lvxing_npc.m4a',
    'rekoe_victim_mentality.m4a',
    'byd_chengshi_zhijia.m4a',
    'dadi_daochenxing_celiang.m4a',
    'changnei_zihe_rensheng.m4a',
    'jiangsida_zhenxiang_nengli.m4a',
    'france_philosophy_bac_truth.m4a',
    'ev21_rag_upgrade_podcast.m4a',
    'suixinfei_66000_worth.m4a',
    'loewe_dangan_ep06.m4a',
    'changxiao_zhongcao_yongzeng.m4a',
    'SpaceX开发史-播客总结.m4a',
]
CONCURRENCY = 2


def is_done(base):
    p = ROOT / f'{base}.txt'
    return p.exists() and p.stat().st_size > 100


def start_one(base):
    log = open(ROOT / f'{base}-whisper.log', 'w')
    p = subprocess.Popen(
        ['python3', str(ROOT / 'scripts' / 'transcribe_one.py'), base, '4'],
        stdout=log, stderr=subprocess.STDOUT)
    print(f'[start] {base} {time.strftime("%H:%M:%S")}', flush=True)
    return p, log


queue = [f[:-4] for f in FILES if not is_done(f[:-4])]
print(f'queue size: {len(queue)}', flush=True)
running = {}

while queue or running:
    while len(running) < CONCURRENCY and queue:
        base = queue.pop(0)
        p, log = start_one(base)
        running[base] = (p, log)
    done_bases = [b for b, (p, _) in running.items() if p.poll() is not None]
    for b in done_bases:
        p, log = running.pop(b)
        log.close()
        if is_done(b):
            print(f'[done] {b} {time.strftime("%H:%M:%S")}', flush=True)
        else:
            print(f'[FAIL] {b} rc={p.returncode}', flush=True)
    if not done_bases:
        time.sleep(20)

print('ALL TRANSCRIPTION DONE', time.strftime('%H:%M:%S'), flush=True)
