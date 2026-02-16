import time
import random


#캐릭터 초기 설정값
INITIAL_GOLD = 1000
INITIAL_POTION = 0
COUNTER_RATE = 0.3
COUNTER_PERCENTAGE = 3
BOSS_CRITICAL_DAMAGE = 2
BOSS_CRITICAL_PERCENTAGE = 3
BERSERK_DAMAGE_RATE = 1.5
BERSERK_TRIGGER_HP = 0.5


#몬스터(자기소개, 공격, 데미지 받음)
class Monster:
  def __init__(self, name, hp, damage):
    self.name = name
    self.hp = hp
    self.max_hp = hp
    self.damage = damage

  def introduce(self):
    print(f"{self.name}가 나타났다! 체력: {self.hp}, 공격력: {self.damage}")

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


#보스몬스터(크리티컬, 광폭화, 셀프 힐)
class BossMonster(Monster):
  def __init__(self, name, hp, damage):
    super().__init__(name, hp, damage)
    self.is_berserk = False

  def take_damage(self, power):         #stronger() 대신 여기다 만들기
    super().take_damage(power)
    if self.hp >0:
      if self.hp < self.max_hp * BERSERK_TRIGGER_HP and self.is_berserk == False:
        self.is_berserk = True
        self.damage *= BERSERK_DAMAGE_RATE
        self.damage = int(self.damage)
        print(f"{self.name}은(는) 발광하기 시작했다! 현재 공격력: {self.damage}\n")
        time.sleep(1)
    else:
      return

  def attack(self, target):         #specialattack 대신 구현
    if random.randint(1,10) < BOSS_CRITICAL_PERCENTAGE:
      print(f"회심의 일격!")
      target.take_damage(self.damage * BOSS_CRITICAL_DAMAGE)
    else:
      super().attack(target)

  def counter_attack(self, target):
    target.take_damage(self.damage*COUNTER_PERCENTAGE)
    print(f"{self.name}은(는) 반격했다! {target.name}에게 {int(self.damage * COUNTER_RATE)}을(를) 피해 입혔다!")

  def heal(self):
    self.hp += int(self.hp/2)
    print(f"{self.name}은(는) 체력을 회복했다! 현재 체력: {self.hp}")


#주인공(공격, 데미지, 스테이터스)
class Adventurer:
  def __init__(self, name, hp, damage):
    self.name = name
    self.hp = hp
    self.max_hp = hp
    self.damage = damage
    self.inventory = []
    self.gold = INITIAL_GOLD
    self.potions = 0

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


  def use_potion(self):
    if self.potions > 0:
      self.potions -= 1
      self.hp += 100  
      if self.hp > self.max_hp:
        self.hp = self.max_hp
      print(f"포션을 마셔서 체력을 100 회복했다! 현재 체력: {self.hp}")
    else:
      print("남은 회복 아이템이 없다!")

  def buy(self, price):
    if self.gold >= price:
      self.gold -= price
      return True
    else:
      print(f"금액이 부족합니다... 필요한 골드: {price}")
      return False
