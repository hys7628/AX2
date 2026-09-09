import sys

def generate_dan(dan: int, limit: int = 9) -> list[tuple[int, int, int]]:
    """
    Generates multiplication table data for a given dan up to the limit.
    Returns list of (dan, multiplier, product).
    """
    if dan < 1:
        raise ValueError("Dan must be a positive integer greater than or equal to 1.")
    if limit < 1:
        raise ValueError("Limit must be a positive integer greater than or equal to 1.")
    
    return [(dan, i, dan * i) for i in range(1, limit + 1)]

def format_dan(dan: int, limit: int = 9) -> str:
    """
    Formats the multiplication table for a single dan.
    """
    lines = [f"=== {dan}단 ==="]
    for d, i, prod in generate_dan(dan, limit):
        lines.append(f"{d} x {i} = {prod}")
    return "\n".join(lines)

def format_all_tables(start: int = 2, end: int = 9, limit: int = 9, cols: int = 4) -> str:
    """
    Formats all tables from start to end in a nice grid with specified column count.
    """
    if start > end:
        raise ValueError("Start dan cannot be greater than end dan.")
        
    all_dans = list(range(start, end + 1))
    result_blocks = []
    
    # Process in chunks of 'cols'
    for chunk_start in range(0, len(all_dans), cols):
        chunk = all_dans[chunk_start:chunk_start + cols]
        
        # Header line
        headers = [f"=== {dan}단 ===".center(16) for dan in chunk]
        block_lines = ["  ".join(headers)]
        
        # Multipliers from 1 to limit
        for i in range(1, limit + 1):
            line_parts = []
            for dan in chunk:
                expr = f"{dan} x {i} = {dan * i}"
                line_parts.append(expr.ljust(16))
            block_lines.append("  ".join(line_parts))
            
        result_blocks.append("\n".join(block_lines))
        result_blocks.append("")  # Empty line between chunks
        
    return "\n".join(result_blocks).strip()

def interactive_mode():
    """
    Runs the gugudan program in interactive mode.
    """
    print("=" * 40)
    print("      ✨ 신나는 구구단 프로그램 ✨")
    print("=" * 40)
    print("1. 특정 단 출력하기")
    print("2. 전체 구구단 출력하기 (2단~9단)")
    print("3. 종료")
    print("-" * 40)
    
    while True:
        try:
            choice = input("선택하고 싶은 메뉴 번호를 입력하세요: ").strip()
            if choice == "1":
                dan_str = input("출력할 단을 입력하세요 (예: 5): ").strip()
                if not dan_str.isdigit():
                    print("❌ 올바른 숫자를 입력해주세요.")
                    continue
                dan = int(dan_str)
                if dan < 1:
                    print("❌ 1 이상의 숫자를 입력해주세요.")
                    continue
                print("\n" + format_dan(dan) + "\n")
            elif choice == "2":
                print("\n" + format_all_tables() + "\n")
            elif choice == "3":
                print("👋 구구단 프로그램을 종료합니다. 감사합니다!")
                break
            else:
                print("❌ 1, 2, 3 중 하나의 번호를 입력해주세요.")
        except (KeyboardInterrupt, EOFError):
            print("\n👋 프로그램을 종료합니다.")
            break

def main():
    if len(sys.argv) > 1:
        # Command line argument mode
        arg = sys.argv[1]
        if arg in ("--help", "-h"):
            print("사용법:")
            print("  python gugudan.py             : 대화형 모드 실행")
            print("  python gugudan.py [단]        : 특정 단 출력 (예: python gugudan.py 5)")
            print("  python gugudan.py all         : 전체 구구단 출력 (2단~9단)")
            return
        
        if arg.lower() == "all":
            print(format_all_tables())
        else:
            try:
                dan = int(arg)
                print(format_dan(dan))
            except ValueError:
                print(f"❌ 올바른 숫자를 입력하시거나 'all'을 입력해주세요. (입력값: {arg})")
                sys.exit(1)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
