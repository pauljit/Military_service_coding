import character as ch
import item
import time
import random
import sys
import data_manager as dm


class GameManager:
  def __init__(self):
    self.hero = ch.Adventurer("모험가", 200, 40)
    saved_data = dm.load_games()
    if saved_data:
      self.hero.name = saved_data["name"]
      self.hero.max_hp = saved_data["max_hp"]
      self.hero.hp = saved_data["hp"]
      self.hero.damage = saved_data["damage"]
      self.hero.gold = saved_data["gold"]
      self.hero.potions = saved_data["potions"]
    else:
      print(f"{self.hero.name}의 새 모험이 시작되었다!")

  def show_main_menu(self):
    while True:
      print("="*10,"[메인메뉴]","="*10)
      print("1. 던전에 입장한다.")
      print("2. 상점을 방문한다.")
      print("3. 여관에서 휴식한다. (50골드)") #매직넘버
      print("4. 게임을 저장한다.")
      print("5. 게임을 끈다.")
      print("="*30)
      menu_choice = self.get_user_input()

      if menu_choice == 1:
        if self.hero.hp > 0:
          self.start_battle()
        else:
          print("체력이 없다.. 여관에서 휴식하자!")
      elif menu_choice == 2:
        self.shop()
      elif menu_choice == 3:
        self.rest()
      elif menu_choice == 4:
        if dm.save_games(self.hero):
          print("게임을 저장했습니다.")
      elif menu_choice == 5:
        print("게임을 종료합니다...")
        sys.exit()
      else:
        print("잘못된 입력입니다. 1, 2, 3, 4, 5 중 하나를 입력하십시오\n")
        continue

  def get_user_input(self):
    while True:
      try:
        value = int(input("선택 >>"))
        return value
      except ValueError:
        print("오류: 잘못된 입력입니다. 숫자를 입력하세요")

  def start_battle(self):
    print(f"던전에 입장했다..\n")
    self.turn = 1
    time.sleep(1)

    mob = ch.BossMonster("쿠카라챠", 100, 20)
    print(f"{mob.name}를 조우했다! 체력: {mob.hp}, 공격력: {mob.damage}")

    while self.hero.hp > 0 and mob.hp > 0:
      print(f"{self.turn}턴 째")
      print("무엇을 할까?(숫자키 입력): 1: 공격   2. 아이템 복용")
      action = self.get_user_input()

      if action == 1:
        self.hero.attack(mob)
      elif action == 2:
        self.hero.use_potion()

      if mob.hp <= 0:
        print(f"\n {mob.name}은(는) 쓰러졌다!")
        #만약 쓰러뜨린 적이 몬스터라면?
        if isinstance(mob, ch.BossMonster):
          self.ending(self.hero)
          break
        break

      print(f"\n--- {mob.name}의 턴 ---")
      mob.attack(self.hero)

      if self.hero.hp <= 0:
        print(f"\n💀 {self.hero.name}은(는) 쓰러졌다...")
        break

      time.sleep(1)
      self.turn += 1

    self.check_result()

  def check_result(self):
    print("="* 30)
    if self.hero.hp > 0:
      self.hero.gold += 300       #매직넘버
      print("300골드를 획득했다!")
    else:
      print("던전에서 도망쳤다...")

  def shop(self):
    print('상점에 방문했다!')
    print(f'상인: "지금은 포션만 취급하고 있습니다..."')
    print(f"무엇을 살까? 1.포션: 300  (0은 취소), 현재 골드 {self.hero.gold}") #매직넘버
    shop_list = self.get_user_input()

    if shop_list == 0:
      print('상인: "다음에 또 오시지요..."')

    elif shop_list == 1:
      if self.hero.buy(300):        #매직넘버
        self.hero.potions += 1
        print(f"포션을 샀다! 현재 포션 개수: {self.hero.potions}\n")
    else:
      print("잘못된 입력입니다. 0,1 중 하나를 선택하십시오")

  def rest(self):
    if self.hero.buy(50):           #매직넘버
      self.hero.hp = self.hero.max_hp
      time.sleep(1)
      print(f"여관에 50골드를 지불하여 체력을 회복하였다! 현재 체력: {self.hero.hp}")   #매직넘버
      print('여관 주인:"다음에 또 오세요!"')
    else:
      print("돈이 부족해서 여관에 쉴 수 없다!")

  def ending(self, main_character):         #보스를 잡으면 엔딩
    print("\n"+"="*30)
    print("그렇게 마을은 평화를 얻었다...")
    time.sleep(0.5)
    print(f"{main_character.name}은 마을의 영웅이 되어 오랜 시간 마을을 지켰다")
    time.sleep(0.5)
    print("END")
    print("dev by 펄짓")
    print("Thanks for play!")
    print("="*30)
    sys.exit()
