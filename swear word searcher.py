z
import json
import os
import sys
import re
from datetime import datetime
from collections import defaultdict

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    BG_RED  = "\033[41m"
    BG_DARK = "\033[40m"

def clr():
    os.system('cls' if os.name == 'nt' else 'clear')



def build_patterns():
    """Строим список скомпилированных regex-паттернов."""

    subs = {
        'а': r'[аa@4аА]',
        'б': r'[бbБ6]',
        'в': r'[вvВ]',
        'г': r'[гgГ]',
        'д': r'[дdД]',
        'е': r'[её3еЕЁ€]',
        'ё': r'[её3еЕЁ€]',
        'ж': r'[жzЖ]',
        'з': r'[з3зЗ]',
        'и': r'[иийiИ1]',
        'й': r'[йиijЙИ]',
        'к': r'[кkКк]',
        'л': r'[лlЛ]',
        'м': r'[мmМ]',
        'н': r'[нnНh]',
        'о': r'[оo0Оoо]',
        'п': r'[пpПn]',
        'р': r'[рrРp]',
        'с': r'[сcСs$5]',
        'т': r'[тtТ]',
        'у': r'[уuyУу]',
        'ф': r'[фfФ]',
        'х': r'[хxhХ]',
        'ц': r'[цcцЦ]',
        'ч': r'[ч4чЧ]',
        'ш': r'[шwШ]',
        'щ': r'[щwщЩ]',
        'ъ': r'[ъьъЪЬ]',
        'ы': r'[ыiыЫ]',
        'ь': r'[ьъьЬЪ]',
        'э': r'[эeэЭ]',
        'ю': r'[юuюЮ]',
        'я': r'[яяЯ]',
        'и': r'[иijИ1]',
        'е': r'[её3еЕЁ]',
    }

    def flex(word):
        """Превращаем слово в regex с заменами букв + возможным растягиванием каждой буквы."""
        result = r'\b'
        for ch in word.lower():
            pat = subs.get(ch, re.escape(ch))
            result += f'(?:{pat})+'
        result += r'\b'
        return result

    roots = [
        (r'(?:[хxhХ])+(?:[уuyУ])+(?:[йijЙ])+', 'stem'),
        (r'(?:[хxhХ])+(?:[уuyУ])+(?:[ёеЁЕё3])+', 'stem'),
        (r'(?:[хxhХ])+(?:[уuyУ])+(?:[яяЯ])+', 'stem'),
        (r'(?:[хxhХ])+(?:[уuyУ])+(?:[иijИ])+', 'stem'),
        (r'(?:[хxhХ])+(?:[уuyУ])+(?:[лlЛ])+(?:[иijИ])+(?:[тtТ])+(?:[ьъЬЪ])*', 'stem'),
        (r'(?:[хxhХ])+(?:[уuyУ])+(?:[еёЕЁ3])+(?:[вВv])+(?:[ыiЫ])+(?:[нnНh])+(?:[ьъЬЪ])*', 'stem'),
        (r'(?:[пpПn])+(?:[иijИ1])+(?:[зЗ3])+(?:[дdД])+', 'stem'),
        (r'(?:[пpПn])+(?:[иijИ1])+(?:[зЗ3])+(?:[дdД])+(?:[аa@4А])+', 'stem'),
        (r'(?:[пpПn])+(?:[еёЕЁ3])+(?:[зЗ3])+(?:[дdД])+', 'stem'),
        (r'(?:[бbБ6])+(?:[лlЛ])+(?:[яяЯ])+(?:[тtТ])+(?:[ьъЬЪ])*', 'stem'),
        (r'(?:[бbБ6])+(?:[лlЛ])+(?:[яяЯ])+(?:[дdД])+(?:[ьъЬЪ])+', 'stem'),
        (r'(?:[бbБ6])+(?:[лlЛ])+(?:[иijИ1])+(?:[нnНh])+', 'stem'),
        (r'(?:[её3еЕЁ])+(?:[бbБ6])+(?:[аa@А4])+(?:[тtТ])+(?:[ьъЬЪ])*', 'stem'),
        (r'(?:[её3еЕЁ])+(?:[бbБ6])+(?:[уuyУ])+(?:[тtТ])*', 'stem'),
        (r'(?:[её3еЕЁ])+(?:[бbБ6])+(?:[аa@А4])+(?:[лlЛ])+', 'stem'),
        (r'(?:[её3еЕЁ])+(?:[бbБ6])+(?:[аa@А4])+(?:[нnНh])+', 'stem'),
        (r'(?:[её3еЕЁ])+(?:[бbБ6])+(?:[иijИ])+', 'stem'),
        (r'(?:[нnНh])+(?:[аa@А4])+(?:[её3еЕЁ])+(?:[бbБ6])+', 'stem'),
        (r'(?:[зЗ3])+(?:[аa@А4])+(?:[её3еЕЁ])+(?:[бbБ6])+', 'stem'),
        (r'(?:[уuyУ])+(?:[её3еЕЁ])+(?:[бbБ6])+', 'stem'),
        (r'(?:[пpПn])+(?:[её3еЕЁ])+(?:[рpРr])+(?:[её3еЕЁ])+(?:[бbБ6])+', 'stem'),
        (r'(?:[её3еЕЁ])+(?:[бbБ6])+(?:[лlЛ])+(?:[аa@А4])+(?:[нnНh])+', 'stem'),
        (r'(?:[её3еЕЁ])+(?:[бbБ6])+(?:[нnНh])+(?:[уuyУ])+(?:[тtТ])+(?:[ьъЬЪ])*', 'stem'),
        (r'(?:[сcСs$5])+(?:[уuyУ])+(?:[кkК])+(?:[аa@А4])+', 'stem'),
        (r'(?:[сcСs$5])+(?:[уuyУ])+(?:[кkК])+(?:[иijИ])+', 'stem'),
        (r'(?:[сcСs$5])+(?:[уuyУ])+(?:[кkК])+(?:[иijИ])+(?:[нnНh])+', 'stem'),
        (r'(?:[мmМ])+(?:[уuyУ])+(?:[дdД])+(?:[аa@А4])+(?:[кkК])+', 'stem'),
        (r'(?:[мmМ])+(?:[уuyУ])+(?:[дdД])+(?:[иijИ1])+(?:[лlЛ])+(?:[аa@А4])+', 'stem'),
        (r'(?:[зЗ3])+(?:[аa@А4])+(?:[лlЛ])+(?:[уuyУ])+(?:[пpПn])+(?:[аa@А4])+', 'stem'),
        (r'(?:[пpПn])+(?:[иijИ1])+(?:[зЗ3])+(?:[дdД])+(?:[её3еЕЁ])+(?:[цcЦ])+', 'stem'),
        (r'(?:[её3еЕЁ])+(?:[бbБ6])+(?:[аa@А4])+(?:[нnНh])+(?:[ыiЫ])+(?:[йijЙ])*', 'stem'),
        (r'(?:[ч4чЧ])+(?:[мmМ])+(?:[оo0О])+', 'stem'),
        (r'(?:[дdД])+(?:[оo0О])+(?:[лlЛ])+(?:[бbБ6])+(?:[оo0О])+(?:[её3еЕЁ])+(?:[бbБ6])+', 'stem'),
        (r'(?:[дdД])+(?:[оo0О])+(?:[лlЛ])+(?:[бbБ6])+(?:[аa@А4])+(?:[её3еЕЁ])+(?:[бbБ6])+', 'stem'),
        (r'(?:[дdД])+(?:[её3еЕЁ])+(?:[бbБ6])+(?:[иijИ1])+(?:[лlЛ])+', 'stem'),
        (r'(?:[иijИ1])+(?:[дdД])+(?:[иijИ1])+(?:[оo0О])+(?:[тtТ])+', 'stem'),
        (r'[бbБ6][9@][тtТ][ьъЬЪ]', 'stem'),
        (r'[бbБ6][лlЛ][яяЯ9][тtТ][ьъЬЪ]*', 'stem'),
        (r'(?:[хxhХ])+(?:[уuyУ])+(?:[её3еЕЁ])+(?:[сcСs])+(?:[оo0О])+(?:[сcСs])+', 'stem'),
        (r'(?:[пpПn])+(?:[иijИ1])+(?:[зЗ3])+(?:[дdД])+(?:[оo0О])+(?:[стрлн])+', 'stem'),
        (r'(?:[шwШ])+(?:[лlЛ])+(?:[уuyУ])+(?:[хxhХ])+(?:[аa@А4])+', 'stem'),
        (r'(?:[пpПn])+(?:[рpРr])+(?:[оo0О])+(?:[сcСs])+(?:[тtТ])+(?:[иijИ1])+(?:[тtТ])+(?:[уuyУ])+(?:[тtТ])+(?:[кkК])+(?:[аa@А4])+', 'stem'),
        (r'(?:[пpПn])+(?:[иijИ1])+(?:[зЗ3])+(?:[дdД])+(?:[юuюЮ])+(?:[кkК])+', 'stem'),
        (r'(?:[её3еЕЁ])+(?:[бbБ6])+(?:[нnНh])+(?:[уuyУ])+(?:[тtТ])+(?:[ыiЫ])+(?:[йijЙ])*', 'stem'),
        (r'(?:[бbБ6])+(?:[зЗ3])+(?:[дdД])+(?:[её3еЕЁ])+(?:[тtТ])+(?:[ьъЬЪ])*', 'stem'),
        (r'(?:[её3еЕЁ])+(?:[бbБ6])+(?:[тtТ])+(?:[ьъЬЪ])*', 'stem'),
        (r'(?:[пpПn])+(?:[оo0О])+(?:[хxhХ])+(?:[уuyУ])+', 'stem'),
        (r'(?:[хxhХ])+(?:[уuyУ])+(?:[яяЯ])+(?:[рpРr])+', 'stem'),
        (r'\b(?:[её3еЕЁ])+(?:[пpПn])+(?:[тtТ])+\b', 'stem'),
        (r'(?:[нnНh])+(?:[аa@А4])+(?:[хxhХ])+(?:[уuyУ])+', 'stem'),
        (r'(?:[пpПn])+(?:[аa@А4])+(?:[хxhХ])+(?:[уuyУ])+', 'stem'),
        (r'(?:[аa@А4])+(?:[хxhХ])+(?:[уuyУ])+(?:[её3еЕЁ])+(?:[тtТ])+(?:[ьъЬЪ])*', 'stem'),
        (r'(?:[оo0О])+(?:[хxhХ])+(?:[уuyУ])+(?:[её3еЕЁ])+(?:[тtТ])+(?:[ьъЬЪ])*', 'stem'),
        (r'(?:[аоаОАoоO0])+(?:[хxhХ])+(?:[уuyУ])+(?:[её3еЕЁ])+(?:[нnНh])+', 'stem'),
        (r'(?:[пpПn])+(?:[иijИ1])+(?:[зЗ3])+(?:[дdД])+(?:[её3еЕЁ])+(?:[жzЖ])+', 'stem'),
        (r'(?:[дdД])+(?:[рpРr])+(?:[оo0О])+(?:[ч4чЧ])+', 'stem'),
        (r'(?:[её3еЕЁ])+(?:[бbБ6])+(?:[нnНh])+(?:[уuyУ])+(?:[тtТ])+(?:[сcСs])+(?:[яяЯ])+', 'stem'),
        (r'(?:[мmМ])+(?:[рpРr])+(?:[аa@А4])+(?:[зЗ3])+(?:[ьъЬЪ])+', 'stem'),
        (r'(?:[тtТ])+(?:[вВv])+(?:[аa@А4])+(?:[рpРr])+(?:[ьъЬЪ])+', 'stem'),
        (r'\b(?:[её3еЕЁ])+(?:[пpПn])+(?:[тtТ])+\b', 'stem'),
        (r'(?:[пpПn])+(?:[её3еЕЁ])+(?:[рpРr])+(?:[дdД])+(?:[её3еЕЁ])+(?:[тtТ])+(?:[ьъЬЪ])*', 'stem'),
        (r'(?:[хxhХ])+(?:[уuyУ])+(?:[яяЯ])+(?:[кkКч4Ч])+', 'stem'),
        (r'(?:[сcСs$5])+(?:[уuyУ])+(?:[ч4чЧ])+(?:[кkК])+(?:[аa@А4])+', 'stem'),
        (r'(?:[вВv])+(?:[ыiЫ])+(?:[бbБ6])+(?:[лlЛ])+(?:[яяЯ])+(?:[дdД])+(?:[оo0О])+(?:[кkК])+', 'stem'),
        (r'(?:[её3еЕЁ])+(?:[бbБ6])+(?:[аa@А4])+(?:[нnНh])+(?:[ыiЫ])+', 'stem'),
        (r'(?:[бbБ6])+(?:[лlЛ])+(?:[яяЯ])+(?:[дtтТ])+(?:[иijИ1])+(?:[нnНh])+(?:[аa@А4])+', 'stem'),
        (r'(?:[нnНh])+(?:[иijИ1])+(?:[хxhХ])+(?:[уuyУ])+', 'stem'),
        (r'(?:[иijИ1])+(?:[зЗ3])+(?:[её3еЕЁ])+(?:[бbБ6])+', 'stem'),
        (r'(?:[оo0О])+(?:[тtТ])+(?:[её3еЕЁ])+(?:[бbБ6])+(?:[иijИ1])+(?:[сcСs$5])+(?:[ьъЬЪ])*', 'stem'),
    ]

    compiled = []
    for pat, _ in roots:
        try:
            compiled.append(re.compile(pat, re.IGNORECASE | re.UNICODE))
        except re.error:
            pass

    return compiled

PATTERNS = build_patterns()


def extract_text(msg):
    text = msg.get('text', '')
    if isinstance(text, str):
        return text
    if isinstance(text, list):
        parts = []
        for item in text:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(item.get('text', ''))
        return ' '.join(parts)
    return ''


def find_mats(text):
    all_matches = []
    for pat in PATTERNS:
        for m in pat.finditer(text):
            word = m.group(0)
            if len(word) >= 3:
                all_matches.append((m.start(), m.end(), word))
    
    if not all_matches:
        return []
    
    all_matches.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    
    result = []
    used = set()
    for start, end, word in all_matches:
        span = set(range(start, end))
        if not span & used:
            result.append(word)
            used |= span
    
    seen = set()
    unique = []
    for w in result:
        wl = w.lower()
        if wl not in seen:
            seen.add(wl)
            unique.append(w)
    return unique


def banner():
    clr()
    print(f"""
{C.RED}{C.BOLD}
 ███╗   ███╗ █████╗ ████████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
 ████╗ ████║██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
 ██╔████╔██║███████║   ██║       ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
 ██║╚██╔╝██║██╔══██║   ██║       ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
 ██║ ╚═╝ ██║██║  ██║   ██║       ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
 ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
{C.RESET}
{C.DIM}             Анализатор матов в Telegram-чате | by codex, by lmuerte{C.RESET}
""")


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def find_json_file():
    """Ищем result.json рядом со скриптом или просим путь."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = ['result.json', 'chat.json', 'messages.json']
    for c in candidates:
        p = os.path.join(script_dir, c)
        if os.path.exists(p):
            return p
    print(f"{C.YELLOW}Файл JSON не найден рядом со скриптом.{C.RESET}")
    print(f"{C.WHITE}Введите полный путь к JSON-файлу экспорта Telegram:{C.RESET}")
    while True:
        path = input(f"{C.CYAN}  Путь > {C.RESET}").strip().strip('"').strip("'")
        if os.path.exists(path):
            return path
        print(f"{C.RED}  Файл не найден. Попробуй ещё раз.{C.RESET}")


def get_users(data):
    """Возвращает список уникальных пользователей (имя, id)."""
    users = {}
    for m in data['messages']:
        frm = m.get('from')
        fid = m.get('from_id')
        if frm and fid:
            users[fid] = frm
    return sorted(users.items(), key=lambda x: x[1].lower())

def select_users(users):
    """Интерактивный выбор пользователей с цифрами."""
    print(f"\n{C.BOLD}{C.WHITE}═══ ПОЛЬЗОВАТЕЛИ ЧАТА ═══{C.RESET}\n")
    
    per_col = 30
    total = len(users)
    
    for i, (uid, name) in enumerate(users):
        num = f"{C.CYAN}[{i+1:3}]{C.RESET}"
        print(f"  {num} {C.WHITE}{name}{C.RESET} {C.DIM}({uid}){C.RESET}")
    
    print(f"\n{C.DIM}Всего пользователей: {total}{C.RESET}")
    print(f"\n{C.YELLOW}Введи номера через запятую или пробел (например: {C.WHITE}1,3,7{C.YELLOW} или {C.WHITE}all{C.YELLOW} для всех):{C.RESET}")
    
    while True:
        choice = input(f"{C.CYAN}  Выбор > {C.RESET}").strip()
        if not choice:
            continue
        
        if choice.lower() in ('all', 'все', '*'):
            return users
        
        parts = re.split(r'[,\s]+', choice)
        selected = []
        valid = True
        for p in parts:
            p = p.strip()
            if not p:
                continue
            try:
                idx = int(p) - 1
                if 0 <= idx < total:
                    selected.append(users[idx])
                else:
                    print(f"{C.RED}  Номер {idx+1} вне диапазона (1-{total}){C.RESET}")
                    valid = False
                    break
            except ValueError:
                print(f"{C.RED}  '{p}' — не число{C.RESET}")
                valid = False
                break
        
        if valid and selected:
            return selected
        elif valid:
            print(f"{C.RED}  Ничего не выбрано{C.RESET}")


def analyze(data, selected_users):
    """Ищем маты от выбранных пользователей. Возвращает dict {uid: [(date, mat, msg_text)]}"""
    target_ids = {uid for uid, name in selected_users}
    results = defaultdict(list)
    
    total = len(data['messages'])
    
    print(f"\n{C.YELLOW}⏳ Анализирую {total:,} сообщений...{C.RESET}", end='', flush=True)
    
    checked = 0
    for m in data['messages']:
        if m.get('type') != 'message':
            continue
        uid = m.get('from_id')
        if uid not in target_ids:
            continue
        
        text = extract_text(m)
        if not text:
            continue
        
        mats = find_mats(text)
        if mats:
            date_raw = m.get('date', '')
            try:
                dt = datetime.fromisoformat(date_raw)
                date_str = dt.strftime('%d.%m.%Y %H:%M')
            except Exception:
                date_str = date_raw
            
            for mat in mats:
                results[uid].append((date_str, mat, text.strip()))
        
        checked += 1
    
    print(f" {C.GREEN}готово!{C.RESET}")
    return results


COLORS_USERS = [C.CYAN, C.MAGENTA, C.GREEN, C.YELLOW, C.BLUE, C.RED]

def print_summary(results, selected_users):
    """Краткая статистика."""
    uid_to_name = {uid: name for uid, name in selected_users}
    
    banner()
    print(f"{C.BOLD}{C.WHITE}═══ РЕЗУЛЬТАТЫ АНАЛИЗА ═══{C.RESET}\n")
    
    grand_total = 0
    for i, (uid, name) in enumerate(selected_users):
        color = COLORS_USERS[i % len(COLORS_USERS)]
        mats = results.get(uid, [])
        count = len(mats)
        grand_total += count
        
        bar_len = min(40, count // max(1, max(len(results.get(u, [])) for u in results or [uid]) // 40 + 1))
        bar = '█' * bar_len
        
        print(f"  {color}{C.BOLD}{name}{C.RESET}")
        print(f"    {color}{bar}{C.RESET} {C.WHITE}{C.BOLD}{count:,}{C.RESET} {C.DIM}матов{C.RESET}")
        print()
    
    print(f"  {C.DIM}{'─'*50}{C.RESET}")
    print(f"  {C.WHITE}Итого: {C.RED}{C.BOLD}{grand_total:,}{C.RESET} {C.WHITE}матов от {len(selected_users)} пользователей{C.RESET}\n")

def print_full_list(results, selected_users):
    """Полный список с датами."""
    uid_to_name = {uid: name for uid, name in selected_users}
    
    print(f"\n{C.BOLD}{C.WHITE}═══ ПОЛНЫЙ СПИСОК МАТОВ ═══{C.RESET}\n")
    
    for i, (uid, name) in enumerate(selected_users):
        color = COLORS_USERS[i % len(COLORS_USERS)]
        mats = results.get(uid, [])
        if not mats:
            continue
        
        print(f"{color}{C.BOLD}{'═'*60}{C.RESET}")
        print(f"{color}{C.BOLD}  {name}  ({len(mats):,} матов){C.RESET}")
        print(f"{color}{C.BOLD}{'═'*60}{C.RESET}")
        
        for date_str, mat, full_text in mats:
            print(f"  {C.DIM}{date_str}{C.RESET}  —  {C.RED}{C.BOLD}{mat}{C.RESET}")
        
        print()

def save_to_file(results, selected_users):
    """Сохраняем полный список в txt."""
    uid_to_name = {uid: name for uid, name in selected_users}
    filename = f"mats_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"Отчёт по матам | {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        for uid, name in selected_users:
            mats = results.get(uid, [])
            if not mats:
                continue
            f.write(f"{name}:\n")
            for date_str, mat, full_text in mats:
                f.write(f"  {date_str} — {mat}\n")
                f.write(f"    Контекст: {full_text[:100]}{'...' if len(full_text)>100 else ''}\n")
            f.write("\n")
    
    print(f"\n{C.GREEN}✓ Сохранено в: {C.WHITE}{C.BOLD}{filename}{C.RESET}")
    return path


def main():
    banner()
    
    print(f"{C.WHITE}Ищу файл экспорта Telegram...{C.RESET}\n")
    json_path = find_json_file()
    
    print(f"{C.GREEN}✓ Файл найден: {C.WHITE}{os.path.basename(json_path)}{C.RESET}")
    print(f"{C.DIM}  Загружаю данные...{C.RESET}", end='', flush=True)
    
    data = load_json(json_path)
    chat_name = data.get('name', 'Чат')
    msg_count = len(data.get('messages', []))
    
    print(f" {C.GREEN}готово!{C.RESET}")
    print(f"\n  {C.CYAN}Чат:{C.RESET} {C.WHITE}{C.BOLD}{chat_name}{C.RESET}")
    print(f"  {C.CYAN}Сообщений:{C.RESET} {C.WHITE}{C.BOLD}{msg_count:,}{C.RESET}\n")
    
    users = get_users(data)
    
    while True:
        banner()
        selected = select_users(users)
        
        banner()
        print(f"{C.WHITE}Выбрано пользователей: {C.BOLD}{len(selected)}{C.RESET}")
        for uid, name in selected:
            print(f"  {C.CYAN}• {name}{C.RESET}")
        
        results = analyze(data, selected)
        
        print_summary(results, selected)
        
        print(f"{C.YELLOW}Хочешь увидеть полный список с датами?{C.RESET}")
        print(f"  {C.WHITE}[1]{C.RESET} — Да, вывести в консоль")
        print(f"  {C.WHITE}[2]{C.RESET} — Да, сохранить в файл .txt")
        print(f"  {C.WHITE}[3]{C.RESET} — И вывести и сохранить")
        print(f"  {C.WHITE}[4]{C.RESET} — Нет, достаточно статистики")
        print(f"  {C.WHITE}[5]{C.RESET} — Выбрать других пользователей")
        print(f"  {C.WHITE}[0]{C.RESET} — Выход\n")
        
        choice = input(f"{C.CYAN}  Выбор > {C.RESET}").strip()
        
        if choice == '1':
            print_full_list(results, selected)
            input(f"\n{C.DIM}Нажми Enter для продолжения...{C.RESET}")
        elif choice == '2':
            save_to_file(results, selected)
            input(f"\n{C.DIM}Нажми Enter для продолжения...{C.RESET}")
        elif choice == '3':
            print_full_list(results, selected)
            save_to_file(results, selected)
            input(f"\n{C.DIM}Нажми Enter для продолжения...{C.RESET}")
        elif choice == '4':
            input(f"\n{C.DIM}Нажми Enter для продолжения...{C.RESET}")
        elif choice == '5':
            continue
        elif choice == '0':
            print(f"\n{C.DIM}Пока! 👋{C.RESET}\n")
            break
        
        banner()
        print(f"\n{C.YELLOW}Что дальше?{C.RESET}")
        print(f"  {C.WHITE}[1]{C.RESET} — Выбрать других пользователей")
        print(f"  {C.WHITE}[0]{C.RESET} — Выход\n")
        again = input(f"{C.CYAN}  Выбор > {C.RESET}").strip()
        if again != '1':
            print(f"\n{C.DIM}Пока! 👋{C.RESET}\n")
            break

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.DIM}Прервано пользователем.{C.RESET}\n")
        sys.exit(0)