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
  def __init__(self, name, heal_amount, price):
    self.name = name
    self.heal_amount = heal_amount

  def __repr__(self):       #출력할 때 이름만 나옴
    return self.name

  def drink(self, person):
    person.hp += self.heal_amount
    if person.hp > person.max_hp:
      person.hp = person.max_hp
    print(f"{self.name}을 마셨다! 현재 체력: {person.hp}")
