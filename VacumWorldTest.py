import random
import numpy as np
from collections import defaultdict


class VacuumWorld:
    """İki konumlu elektrikli süpürge dünyası ortamı"""

    def __init__(self):
        self.locations = ['A', 'B']
        self.reset()

    def reset(self):
        """Ortamı rastgele başlangıç durumuna getirir"""
        self.state = {
            'A': random.choice([True, False]),  # True = Kirli, False = Temiz
            'B': random.choice([True, False]),
            'position': random.choice(self.locations)
        }
        return self.state.copy()

    def is_dirty(self, location):
        """Belirtilen konumun kirli olup olmadığını kontrol eder"""
        return self.state[location]

    def clean(self, location):
        """Belirtilen konumu temizler"""
        self.state[location] = False

    def move(self, new_location):
        """Ajanı yeni konuma taşır"""
        self.state['position'] = new_location

    def is_clean(self):
        """Tüm ortamın temiz olup olmadığını kontrol eder"""
        return not self.state['A'] and not self.state['B']

    def get_state(self):
        return self.state.copy()


class RandomAgent:
    """Rastgele eylem seçen ajan"""

    def __init__(self):
        self.name = "Rastgele Ajan"

    def decide_action(self, state):
        """Rastgele bir eylem seçer: Suck, Left, Right"""
        return random.choice(['Suck', 'Left', 'Right'])


class TableBasedAgent:
    """Tablo tabanlı ajan - tüm durumlar için önceden tanımlı eylemler"""

    def __init__(self):
        self.name = "Tablo Tabanlı Ajan"
        # Her durum için en iyi eylemi tanımla
        self.table = {
            ('A', True, True): 'Suck',
            ('A', True, False): 'Suck',
            ('A', False, True): 'Right',
            ('A', False, False): 'Right',
            ('B', True, True): 'Suck',
            ('B', True, False): 'Suck',
            ('B', False, True): 'Left',
            ('B', False, False): 'Left',
        }

    def decide_action(self, state):
        """Tablodan uygun eylemi seçer"""
        key = (state['position'], state['A'], state['B'])
        return self.table.get(key, 'Suck')


class ReflexAgent:
    """Refleks ajan - mevcut algıya göre karar verir"""

    def __init__(self):
        self.name = "Refleks Ajan"

    def decide_action(self, state):
        """Basit kurallarla eylem seçer"""
        current_pos = state['position']

        # Bulunduğu yer kirliyse temizle
        if state[current_pos]:
            return 'Suck'

        # Değilse diğer yere git
        if current_pos == 'A':
            return 'Right'
        else:
            return 'Left'


class ModelBasedAgent:
    """Model tabanlı ajan - geçmiş durumları takip eder"""

    def __init__(self):
        self.name = "Model Tabanlı Ajan"
        self.model = {'A': None, 'B': None}  # İç dünya modeli
        self.last_position = None

    def reset(self):
        """Her simülasyon için hafızayı sıfırla"""
        self.model = {'A': None, 'B': None}
        self.last_position = None

    def update_model(self, state):
        """İç modeli güncelle"""
        current_pos = state['position']
        self.model[current_pos] = state[current_pos]
        self.last_position = current_pos

    def decide_action(self, state):
        """Model bilgisine göre karar ver"""
        self.update_model(state)
        current_pos = state['position']

        # Bulunduğu yer kirliyse temizle
        if state[current_pos]:
            return 'Suck'

        # Diğer yerin durumuna göre karar ver
        other_pos = 'B' if current_pos == 'A' else 'A'

        # Eğer diğer yerin kirli olduğunu biliyorsa oraya git
        if self.model[other_pos] is True:
            return 'Right' if current_pos == 'A' else 'Left'

        # Diğer yeri hiç görmediyse oraya git
        if self.model[other_pos] is None:
            return 'Right' if current_pos == 'A' else 'Left'

        # Her yer temizse rastgele hareket et
        return random.choice(['Left', 'Right'])


def run_simulation(agent, world, max_actions=10):
    """Tek bir simülasyon çalıştırır"""
    state = world.reset()

    # Model tabanlı ajan için hafızayı sıfırla
    if hasattr(agent, 'reset'):
        agent.reset()

    for _ in range(max_actions):
        action = agent.decide_action(state)

        if action == 'Suck':
            world.clean(state['position'])
        elif action == 'Left':
            world.move('A')
        elif action == 'Right':
            world.move('B')

        state = world.get_state()

        # Her yer temizse erken bitir
        if world.is_clean():
            break

    return world.is_clean()


def run_experiments(num_trials=10):
    """Tüm ajanlar için deneyleri çalıştırır"""
    world = VacuumWorld()
    agents = [
        RandomAgent(),
        TableBasedAgent(),
        ReflexAgent(),
        ModelBasedAgent()
    ]

    results = {}

    print("=" * 60)
    print("ELEKTRİKLİ SÜPÜRGE DÜNYASI - PERFORMANS ANALİZİ")
    print("=" * 60)
    print(f"\nSimülasyon Parametreleri:")
    print(f"  - Deneme Sayısı: {num_trials}")
    print(f"  - Her denemede maksimum eylem sayısı: 10")
    print(f"  - Konumlar: A ve B")
    print(f"  - Başarı kriteri: Her iki konumun da temiz olması\n")

    for agent in agents:
        successes = 0
        print(f"\n{agent.name} Test Ediliyor...")
        print("-" * 60)

        for trial in range(num_trials):
            success = run_simulation(agent, world, max_actions=10)
            successes += success
            status = "✓ BAŞARILI" if success else "✗ BAŞARISIZ"
            print(f"  Deneme {trial + 1:2d}: {status}")

        success_rate = (successes / num_trials) * 100
        results[agent.name] = {
            'successes': successes,
            'success_rate': success_rate
        }

        print(f"\n  Toplam Başarı: {successes}/{num_trials}")
        print(f"  Başarı Oranı: {success_rate:.1f}%")

    # Sonuçları karşılaştır
    print("\n" + "=" * 60)
    print("KARŞILAŞTIRMALI SONUÇLAR")
    print("=" * 60)

    sorted_results = sorted(results.items(), key=lambda x: x[1]['success_rate'], reverse=True)

    print(f"\n{'Ajan Tipi':<25} {'Başarı Sayısı':<15} {'Başarı Oranı'}")
    print("-" * 60)

    for name, data in sorted_results:
        bar = '█' * int(data['success_rate'] / 5)
        print(f"{name:<25} {data['successes']:>2}/{num_trials:<10} {data['success_rate']:>5.1f}% {bar}")

    # Analiz
    print("\n" + "=" * 60)
    print("ANALİZ VE YORUM")
    print("=" * 60)

    best_agent = sorted_results[0][0]
    worst_agent = sorted_results[-1][0]

    print(f"\n1. En başarılı ajan: {best_agent}")
    print(f"   Başarı oranı: {sorted_results[0][1]['success_rate']:.1f}%")

    print(f"\n2. En düşük performans: {worst_agent}")
    print(f"   Başarı oranı: {sorted_results[-1][1]['success_rate']:.1f}%")

    return results


if __name__ == "__main__":
    results = run_experiments(num_trials=10)