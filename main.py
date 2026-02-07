import time
import random

# --- [게임 설정값] (Magic Numbers 제거) ---
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


# --- [클래스 정의] ---
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
        self.hp = int(self.hp)
        print(f"{self.name}에게 {power}의 데미지를 입혔다!")
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
        damage = self.damage * BOSS_CRITICAL_DAMAGE
        target.take_damage(damage)
        print(f"회심의 일격! {self.name}은(는) {target.name}에게 {damage}을(를) 피해 입혔다!")

    def counter_attack(self, target):
        damage = int(self.damage * COUNTER_RATE)
        target.take_damage(damage)
        print(f"{self.name}은(는) 반격했다! {target.name}에게 {damage}을(를) 피해 입혔다!")

    def stronger(self):
        if not self.is_berserk:
            self.is_berserk = True
            self.damage *= BERSERK_DAMAGE_RATE
            self.damage = int(self.damage)
            print(f"{self.name}은(는) 발광하기 시작했다! 현재 공격력: {self.damage}\n")
            time.sleep(1)

    def heal(self):
        self.hp += int(self.hp / 2)
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
        self.hp = int(self.hp)
        print(f"{self.name}에게 {power}의 데미지를 받았다!")
        if self.hp <= 0:
            self.hp = 0
            print(f"{self.name}의 남은 체력: {self.hp}")
            print(f"{self.name}은(는) 쓰러졌다...\n")
        else:
            print(f"{self.name}의 남은 체력: {self.hp}\n")

    def status(self):
        print("=" * 30)
        print(f"이름: {self.name}")
        print(f"체력: {self.hp}/{self.max_hp}")
        print(f"공격력: {self.damage}")
        print(f"골드: {self.gold}")
        print(f"가방: {self.inventory}")
        print("=" * 30)

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
        for item in self.inventory:
            if isinstance(item, HealItem):
                item.drink(self)
                self.inventory.remove(item)
                return True
        print("남은 회복 아이템이 없다!")
        return False


class Weapon:
    def __init__(self, name, attack_up):
        self.name = name
        self.attack_up = attack_up

    def __repr__(self):
        return self.name

    def equip(self, person):
        person.damage += self.attack_up
        print(f"{self.name}을 장착했다!")
        print(f"현재 공격력: {person.damage}")


class HealItem:
    def __init__(self, name, heal_amount):
        self.name = name
        self.heal_amount = heal_amount

    def __repr__(self):
        return self.name

    def drink(self, person):
        person.hp += self.heal_amount
        if person.hp > person.max_hp:
            person.hp = person.max_hp
        print(f"{self.name}을 마셨다! 현재 체력: {person.hp}")


# --- [상점 방문] ---
def visit_shop(customer):
    print("\n[상점] 떠돌이 마차 상점에 방문했다!")
    print('상점 주인: "무엇이든 취급합니다..."')
    print(f"1. 아이언 메이스(공격력 + {MACE_DEAL}) 가격: {MACE_PRICE}")
    print(f"2. 오렌지 포션(체력 + {POTION_HEAL_AMOUNT}) 가격: {POTION_PRICE}")
    
    while True:
        try:
            choice = int(input("숫자를 입력해 필요한 아이템을 구매하세요 (0: 나가기) >> "))
            if choice == 1:
                customer.buy(iron_mace, MACE_PRICE)
            elif choice == 2:
                customer.buy(orange_potion, POTION_PRICE)
            elif choice == 0:
                print("마차 상점을 나갔다.\n")
                break
            else:
                print("잘못된 입력입니다.")
        except ValueError:
            print("숫자를 입력해주세요!")


def battle_start(hero, enemy):
    enemy.introduce()
    while True:
        print(f"\n[{hero.name} HP: {hero.hp}] vs [{enemy.name} HP: {enemy.hp}]")
        try:
            attack_or_drink = int(input("행동 선택 (1: 싸운다, 2: 회복 아이템 사용) >> "))
        except ValueError:
            print("숫자를 입력해주세요!")
            continue

        if attack_or_drink == 1:
            hero.attack(enemy)
            if isinstance(enemy, BossMonster):
                if enemy.hp <= 0:
                    break
                elif enemy.hp <= enemy.max_hp * BERSERK_TRIGGER_HP:
                    enemy.stronger()
                elif COUNTER_PERCENTAGE >= random.randint(1, 10):
                    enemy.counter_attack(hero)

        elif attack_or_drink == 2:
            result = hero.use_potion()
            if result == False:
                continue
        else:
            print("잘못된 입력입니다.")
            continue

        if enemy.hp <= 0:
            print("\n🎉 주인공은 승리했다!")
            break

        time.sleep(1)
        
        # 보스 턴 (반격 안 했을 때 or 반격 후 추가타 - 기획의도)
        if isinstance(enemy, BossMonster) and enemy.hp > 0:
            if BOSS_CRITICAL_PERCENTAGE >= random.randint(1, 10):
                enemy.special_attack(hero)
            else:
                enemy.attack(hero)
        elif enemy.hp > 0:
            enemy.attack(hero)

        time.sleep(1)
        
        if hero.hp <= 0:
            print("\n💀 주인공은 패배했다...")
            break


# --- [게임 실행] ---
if __name__ == "__main__":
    # 아이템 세팅 (전역 변수로 사용하기 위해 미리 선언)
    iron_mace = Weapon("아이언 메이스", MACE_DEAL)
    orange_potion = HealItem("오렌지 포션", POTION_HEAL_AMOUNT)

    hero = Adventurer("모험가", 300, 60)
    
    # 게임 시작
    hero.status()
    visit_shop(hero)
    
    mob2 = BossMonster("러스티 크라운", 300, 30)
    battle_start(hero, mob2)
