import json
import os
import game_manager as gm
import character as ch

SAVE_FILE = "sava_data.json"


def save_games(hero):     #주인공 info 저장
  data = {
      "name" : hero.name,
      "max_hp" : hero.max_hp,
      "hp" : hero.hp,
      "damage" : hero.damage,
      "gold" :  hero.gold,
      "potions" : hero.potions
  }

  try:
    with open(SAVE_FILE, "w", encoding='utf-8') as f:       #write 모드로 SAVE_FILE 경로에 utf-8 형식으로 작성
      json.dump(data, f,ensure_ascii = False, indent = 4)
    print(f"{hero.name}의 게임 내용을 저장했습니다.")
    return True
  except Exception as e:
    print(f"게임 내용을 저장하는 데 실패했습니다! 에러 내용: {e}")
    return False

def load_games():
  if not os.path.exists(SAVE_FILE):
    return None

  try:
    with open(SAVE_FILE, "r", encoding='utf-8') as f:
      data = json.load(f)
    print(f"게임을 불러왔습니다. 환영합니다, {data["name"]}님")
    return data
  except Exception as e:
    print(f"게임 내용을 불러오는 데 실패했습니다! 에러내용: {e}")
    return None
