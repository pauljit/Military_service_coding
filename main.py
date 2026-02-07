# 17일차 (2/6) (가독성 upgrade (PEP8))

import random
import time

#magic number을 배제한 게임 설정값 (모든 글자는 대문자, 띄어쓰기는 _)
INITIAL_GOLD = 1000
MACE_PRICE = 1000
MACE_DEAL = 10
POTION_PRICE = 300
POTION_HEAL_AMOUNT = 100
COUNTER_RATE = 0.3
COUNTER_PERCENTAGE = 3
BOSS_CRITICAL_DAMAGE = 3
BOSS_CRITICAL_PERCENTAGE = 3
BERSERK_DAMAGE_RATE = 1.5
BERSERK_TRIGGER_HP = 0.5


class Monster:
  def __init__(self, name, hp, damage):
    self.name = name
    self.hp = hp
    self.max_hp = hp
    self.damage = damage

  def introduce(self):
    print(f"{self.name}: 체력: {self.hp}, 공격력: {self.damage}")

  def attack(self, target):
    print(f"{self.name}의 공격!")
    target.take_damage(self.damage)

  def take_damage(self, power):
    self.hp -= power
    int(self.hp)
    print(f"\n{self.name}에게 {power}의 데미지를 입혔다!")
    if self.hp <= 0:
      self.hp = 0
      print(f"{self.name}의 남은 체력: {self.hp}")
      print(f"{self.name}을 쓰러뜨렸다!\n")
    else:
      print(f"{self.name}의 남은 체력: {self.hp}\n")


class BossMonster(Monster):
  def __init__(self, name, hp, damage):
    super().__init__(name, hp, damage)
    self.is_berserk = False

  def special_attack(self, target):
    target.take_damage(self.damage * BOSS_CRITICAL_DAMAGE)
    print(f"회심의 일격! {self.name}은(는) {target.name}에게 {self.damage * BOSS_CRITICAL_DAMAGE}을(를) 피해 입혔다!")
    time.sleep(1)

  def counter_attack(self, target):
    target.take_damage(self.damage*COUNTER_PERCENTAGE)
    print(f"{self.name}은(는) 반격했다! {target.name}에게 {int(self.damage * 0.3)}을(를) 피해 입혔다!")

  def stronger(self):
    if self.is_berserk == False:
      self.is_berserk = True
      self.damage *= BERSERK_DAMAGE_RATE
      self.damage = int(self.damage)
      print(f"{self.name}은(는) 발광하기 시작했다! 현재 공격력: {self.damage}\n")
      time.sleep(1)
    else:
      return

  def heal(self):
    self.hp += int(self.hp/2)
    print(f"{self.name}은(는) 체력을 회복했다! 현재 체력: {self.hp}")


class Adventurer:
  def __init__(self, name, hp, damage):
    self.name = name
    self.hp = hp
    self.max_hp = hp
    self.damage = damage
    self.inventory = []
    self.gold = INITIAL_GOLD

  def attack(self, enemy):
    print(f"{self.name}은(는) {enemy.name}을 공격했다!")
    enemy.take_damage(self.damage)

  def take_damage(self, power):
    self.hp -= power
    int(self.hp)
    print(f"{self.name}에게 {power}의 데미지를 받았다!")
    if self.hp <= 0:
      self.hp = 0
      print(f"{self.name}의 남은 체력: {self.hp}")
      print(f"{self.name}은(는) 쓰러졌다...\n")
    else:
      print(f"{self.name}의 남은 체력: {self.hp}\n")

  def status(self):
    print("="*30)
    print(f"이름: {self.name}")
    print(f"체력: {self.hp}/{self.max_hp}")
    print(f"공격력: {self.damage}")
    print(f"골드: {self.gold}")
    print(f"가방: {self.inventory}")
    print("="*30)

  def buy(self, item, price):
    if self.gold >= price:
      self.gold -= price
      self.inventory.append(item)
      print(f"{item}을 구입했다! 보유 골드: {self.gold}")
      if isinstance(item, Weapon):
        item.equip(self)
    else:
      print(f"골드가 부족합니다. 보유 골드: {self.gold}, 가격: {price}")

  def use_potion(self):
    for item in self.inventory:           #포션이 있을 경우 마심
      if isinstance(item, Heal_item):
        item.drink(self)
        self.inventory.remove(item)
        return True
    print("남은 회복 아이템이 없다!")
    return False


class Weapon:                 #무기 장착 시 공격력 강화
  def __init__(self, name, attack_up):
    self.name = name
    self.attack_up = attack_up

  def __repr__(self):       #출력할 때 이름만 나옴
    return self.name

  def equip(self, person):
    person.damage += self.attack_up
    print(f"{self.name}을 장착했다!")
    print(f"현재 공격력: {person.damage}")


class HealItem:             #포션 복용 시 체력 회복
  def __init__(self, name, heal_amount):
    self.name = name
    self.heal_amount = heal_amount

  def __repr__(self):       #출력할 때 이름만 나옴
    return self.name

  def drink(self, person):
    person.hp += self.heal_amount
    if person.hp > person.max_hp:
      person.hp = person.max_hp
    print(f"{self.name}을 마셨다! 현재 체력: {person.hp}")


def visit_shop(customer):
  print("떠돌이 마차 상점에 방문했다!")
  print('상점 주인: "무엇이든 취급합니다...')
  print(f"1. 아이언 메이스(공격력 + {MACE_DEAL}) 가격: {MACE_PRICE}")
  print(f"2. 오렌지 포션(체력 + {POTION_HEAL_AMOUNT}) 가격: {POTION_PRICE}")
  choice = int(input("숫자를 입력해 필요한 아이템을 구매하세요.(나가려면 0 입력)"))
  if choice == 1:
    customer.buy(iron_mace, MACE_PRICE)
  elif choice == 2:
    customer.buy(orange_potion, POTION_PRICE)
  elif choice == 0:
    print("마차 상점을 나갔다")
  else:
    print("잘못된 입력입니다. 원하는 상품의 숫자나 0을 입력하십시오")
  print('상점 주인: "다음에 또 뵙겠습니다..."')
  print("상점을 나왔다.\n")

def battle_start(hero, enemy):
  enemy.introduce()
  while True:
    attack_or_drink = int(input("어떻게 할까?(1: 싸운다,   2: 회복 아이템을 쓴다)"))

    if attack_or_drink == 1:
      hero.attack(enemy)                        #영웅이 먼저 공격
      if isinstance(enemy, BossMonster):       #만약 적이 보스면
        if enemy.hp <= 0:                       #적이 죽으면 뭘 하기도 전에 끝
          break
        elif enemy.hp <= enemy.max_hp * BERSERK_TRIGGER_HP:   #광폭화 트리거 hp 비율에 다다름
          enemy.stronger()
        elif COUNTER_PERCENTAGE >= random.randint(1, 10):       #공격 받은 직후 일정 확률로 반격
          enemy.counter_attack(hero)

    elif attack_or_drink == 2:              #회복 아이템 사용
      result = hero.use_potion()
      if result == False:
       continue
    else:
      print("잘못된 입력입니다. 선택지에 포함된 숫자를 입력하십시오")
      continue

    if enemy.hp <= 0:
      print("\n주인공은 승리했다!")
      break

    elif isinstance(enemy, BossMonster):
      if BOSS_CRITICAL_PERCENTAGE >= random.randint(1, 10):
        enemy.special_attack(hero)
      else: enemy.attack(hero)

    else:            #일반 몹이 공격
      enemy.attack(hero)


    if hero.hp <= 0:
      print("\n 주인공은 패배했다...")
      break


# 게임 진행
hero = Adventurer("모험가", 300, 60)
mob2 = BossMonster("러스티 크라운", 300, 30)
iron_mace = Weapon("아이언 메이스", MACE_DEAL)
orange_potion = HealItem("오렌지 포션", POTION_HEAL_AMOUNT)


visit_shop(hero)

time.sleep(1)

mob2 = BossMonster("러스티 크라운", 300, 30)
battle_start(hero, mob2)
