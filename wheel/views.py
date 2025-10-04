import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# ฟังก์ชันสำหรับแสดงหน้าเว็บหลัก
def wheel_page(request):
    # สั่งให้ Django ไปหาไฟล์ index.html มาแสดงผล
    return render(request, 'wheel/index.html')

# API สำหรับการหมุนวงล้อ
@csrf_exempt # ใช้เพื่อทดสอบง่ายๆ (ในการใช้งานจริงควรใช้ CSRF token)
def spin_wheel(request):
    # รับ request แบบ POST จาก JavaScript เท่านั้น
    if request.method == 'POST':
        try:
            # แปลงข้อมูลที่ส่งมา (JSON) ให้ Python รู้จัก
            data = json.loads(request.body)
            names = data.get('names', [])
            predetermined_winner = data.get('winner', None)

            if not names:
                return JsonResponse({'error': 'No names provided'}, status=400)

            winner_name = None
            winner_index = -1

            # Logic การตัดสินผู้ชนะ
            if predetermined_winner and predetermined_winner in names:
                # ถ้ามีการกำหนดผู้ชนะ และชื่อนั้นอยู่ในลิสต์
                winner_name = predetermined_winner
                winner_index = names.index(predetermined_winner)
            else:
                # ถ้าไม่มีการกำหนด ก็สุ่มเอา
                winner_index = random.randint(0, len(names) - 1)
                winner_name = names[winner_index]

            # ส่งผลลัพธ์กลับไปเป็น JSON ให้ JavaScript
            return JsonResponse({
                'winner': winner_name,
                'winnerIndex': winner_index
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)