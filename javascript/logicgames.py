import pygame
import sys
import random
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 50

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 150, 255)
YELLOW = (255, 255, 100)
ORANGE = (255, 180, 100)
PURPLE = (180, 100, 255)
CYAN = (100, 255, 255)
BROWN = (139, 90, 43)
DARK_BROWN = (101, 67, 33)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Logic Gates Adventure")
clock = pygame.time.Clock()

font_large = pygame.font.Font(None, 64)
font_medium = pygame.font.Font(None, 42)
font_small = pygame.font.Font(None, 32)
font_tiny = pygame.font.Font(None, 24)

# Optional wall image (look in several common asset locations). If found, it's
# scaled to the tile interior size and used when rendering '#' tiles.
WALL_IMAGE = None
# Look for common wall image names in the script directory and a few subfolders.
script_dir = os.path.dirname(os.path.abspath(__file__))
candidates = [
    "walls.jpg",
    os.path.join("assets", "wall.png"), os.path.join("assets", "walls.png"),
]
for name in candidates:
    path = os.path.join(script_dir, name) if not os.path.isabs(name) else name
    try:
        if os.path.isfile(path):
            img = pygame.image.load(path).convert_alpha()
            WALL_IMAGE = pygame.transform.smoothscale(img, (TILE_SIZE, TILE_SIZE))
            print(f"Loaded wall image: {path}")
            break
    except Exception as e:
        print(f"Failed loading wall image '{path}': {e}")

if WALL_IMAGE is None:
    print("No wall image found — using colored rectangles for walls.")

LEVELS = [
    {
        "name": "Level 1 - Getting Started",
        "layout": [
            "########",
            "#      #",
            "#  @   #",
            "#  $   #",
            "#  .   #",
            "#      #",
            "########",
        ],
        "gate": "AND"
    },
    {
        "name": "Level 2 - Two Boxes",
        "layout": [
            "##############",
            "#     ##     #",
            "# $   ##   $ #",
            "#  $  ##  $  #",
            "#     @      #",
            "##### ## #####",
            "#.  .    .  .#",
            "##############",
        ],
        "gate": "OR"
    },
    {
        "name": "Level 3 - Corner Push",
        "layout": [
            "##########",
            "#        #",
            "# $  # $ #",
            "#  @ #   #",
            "#### # # #",
            "#.   .   #",
            "##########",
        ],
        "gate": "NOT"
    },
    {
        "name": "Level 4 - Two Rooms",
        "layout": [
            "###########",
            "#    #    #",
            "# $  # $  #",
            "#  # # #  #",
            "#  # @ #  #",
            "#  #####  #",
            "# .     . #",
            "###########",
        ],
        "gate": "NAND"
    },
    {
        "name": "Level 5 - The Maze",
        "layout": [
            "########",
            "## @####",
            "## $  ##",
            "### # ##",
            "#.# #  #",
            "#.$  # #",
            "#.   $ #",
            "########",
        ],
        "gate": "NOR"
    },
    {
        "name": "Level 6 - The Threat",
        "layout": [
            "########",
            "###    #",
            "###$$$ #",
            "#  $.. #",
            "#@$...##",
            "####  ##",
            "########",
        ],
        "gate": "XOR"
    },
    {
        "name": "Level 7 - Final Challenge",
        "layout": [
            "########",
            "#####  #",
            "###. $ #",
            "#..$ $ #",
            "#.  $#@#",
            "###    #",
            "#####  #",
            "########",
        ],
        "gate": "XNOR"
    }
]

LOGIC_GATES = {
    "AND": {
        "name": "AND Gate",
        "symbol": "A AND B = Y",
        "description": "The AND gate outputs TRUE (1) only when ALL inputs are TRUE (1). If any input is FALSE (0), the output is FALSE (0).",
        "truth_table": [
            ("A", "B", "Y"),
            ("0", "0", "0"),
            ("0", "1", "0"),
            ("1", "0", "0"),
            ("1", "1", "1"),
        ],
        "real_world": "Like a security door that needs BOTH a key card AND a PIN code to open."
    },
    "OR": {
        "name": "OR Gate",
        "symbol": "A OR B = Y",
        "description": "The OR gate outputs TRUE (1) when AT LEAST ONE input is TRUE (1). It only outputs FALSE (0) when ALL inputs are FALSE (0).",
        "truth_table": [
            ("A", "B", "Y"),
            ("0", "0", "0"),
            ("0", "1", "1"),
            ("1", "0", "1"),
            ("1", "1", "1"),
        ],
        "real_world": "Like a room with two light switches - either switch can turn on the light."
    },
    "NOT": {
        "name": "NOT Gate (Inverter)",
        "symbol": "NOT A = Y",
        "description": "The NOT gate (inverter) has only ONE input. It outputs the OPPOSITE of the input. TRUE becomes FALSE, and FALSE becomes TRUE.",
        "truth_table": [
            ("A", "Y"),
            ("0", "1"),
            ("1", "0"),
        ],
        "real_world": "Like a light switch - when it's ON, it turns OFF and vice versa."
    },
    "NAND": {
        "name": "NAND Gate",
        "symbol": "A NAND B = Y",
        "description": "The NAND gate is an AND gate followed by a NOT gate. It outputs FALSE (0) only when ALL inputs are TRUE (1). Otherwise, it outputs TRUE (1).",
        "truth_table": [
            ("A", "B", "Y"),
            ("0", "0", "1"),
            ("0", "1", "1"),
            ("1", "0", "1"),
            ("1", "1", "0"),
        ],
        "real_world": "Like a safety system that triggers an alarm unless ALL conditions are normal."
    },
    "NOR": {
        "name": "NOR Gate",
        "symbol": "A NOR B = Y",
        "description": "The NOR gate is an OR gate followed by a NOT gate. It outputs TRUE (1) only when ALL inputs are FALSE (0). Any TRUE input makes the output FALSE.",
        "truth_table": [
            ("A", "B", "Y"),
            ("0", "0", "1"),
            ("0", "1", "0"),
            ("1", "0", "0"),
            ("1", "1", "0"),
        ],
        "real_world": "Like a 'quiet mode' that activates only when ALL noise sources are off."
    },
    "XOR": {
        "name": "XOR Gate (Exclusive OR)",
        "symbol": "A XOR B = Y",
        "description": "The XOR gate outputs TRUE (1) when the inputs are DIFFERENT. It outputs FALSE (0) when both inputs are the SAME.",
        "truth_table": [
            ("A", "B", "Y"),
            ("0", "0", "0"),
            ("0", "1", "1"),
            ("1", "0", "1"),
            ("1", "1", "0"),
        ],
        "real_world": "Like a hallway with switches at both ends - flipping either switch changes the light state."
    },
    "XNOR": {
        "name": "XNOR Gate (Exclusive NOR)",
        "symbol": "A XNOR B = Y",
        "description": "The XNOR gate outputs TRUE (1) when both inputs are the SAME. It outputs FALSE (0) when the inputs are DIFFERENT.",
        "truth_table": [
            ("A", "B", "Y"),
            ("0", "0", "1"),
            ("0", "1", "0"),
            ("1", "0", "0"),
            ("1", "1", "1"),
        ],
        "real_world": "Like a comparison checker - it says 'match' when both inputs are equal."
    }
}

QUIZ_QUESTIONS = {
    "AND": [
        {"question": "What is the output of AND gate when A=1 and B=1?", "options": ["0", "1"], "answer": "1"},
        {"question": "AND gate outputs 1 only when:", "options": ["All inputs are 1", "Any input is 1", "All inputs are 0"], "answer": "All inputs are 1"},
        {"question": "What is 0 AND 1?", "options": ["0", "1"], "answer": "0"},
    ],
    "OR": [
        {"question": "What is the output of OR gate when A=0 and B=1?", "options": ["0", "1"], "answer": "1"},
        {"question": "OR gate outputs 0 only when:", "options": ["All inputs are 0", "Any input is 0", "All inputs are 1"], "answer": "All inputs are 0"},
        {"question": "What is 1 OR 0?", "options": ["0", "1"], "answer": "1"},
    ],
    "NOT": [
        {"question": "What is NOT 1?", "options": ["0", "1"], "answer": "0"},
        {"question": "What is NOT 0?", "options": ["0", "1"], "answer": "1"},
        {"question": "NOT gate is also called:", "options": ["Inverter", "Buffer", "Amplifier"], "answer": "Inverter"},
    ],
    "NAND": [
        {"question": "What is 1 NAND 1?", "options": ["0", "1"], "answer": "0"},
        {"question": "NAND is equivalent to:", "options": ["NOT(AND)", "NOT(OR)", "AND(NOT)"], "answer": "NOT(AND)"},
        {"question": "What is 0 NAND 0?", "options": ["0", "1"], "answer": "1"},
    ],
    "NOR": [
        {"question": "What is 0 NOR 0?", "options": ["0", "1"], "answer": "1"},
        {"question": "NOR gate outputs 1 only when:", "options": ["All inputs are 0", "Any input is 0", "All inputs are 1"], "answer": "All inputs are 0"},
        {"question": "What is 1 NOR 0?", "options": ["0", "1"], "answer": "0"},
    ],
    "XOR": [
        {"question": "What is 1 XOR 1?", "options": ["0", "1"], "answer": "0"},
        {"question": "XOR outputs 1 when:", "options": ["Inputs are different", "Inputs are same", "All inputs are 1"], "answer": "Inputs are different"},
        {"question": "What is 0 XOR 1?", "options": ["0", "1"], "answer": "1"},
    ],
    "XNOR": [
        {"question": "What is 1 XNOR 1?", "options": ["0", "1"], "answer": "1"},
        {"question": "XNOR outputs 1 when:", "options": ["Inputs are same", "Inputs are different", "Any input is 1"], "answer": "Inputs are same"},
        {"question": "What is 0 XNOR 1?", "options": ["0", "1"], "answer": "0"},
    ]
}

class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=CYAN, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=10)
        
        text_surface = font_medium.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class SokobanGame:
    def __init__(self, level_index):
        self.level_index = level_index
        self.load_level()
    
    def load_level(self):
        level_data = LEVELS[self.level_index]
        self.layout = [list(row) for row in level_data["layout"]]
        self.gate = level_data["gate"]
        self.height = len(self.layout)
        self.width = max(len(row) for row in self.layout)
        
        self.player_pos = None
        self.boxes = []
        self.targets = []
        self.walls = []
        
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == '@':
                    self.player_pos = [x, y]
                    self.layout[y][x] = ' '
                elif cell == '$':
                    self.boxes.append([x, y])
                    self.layout[y][x] = ' '
                elif cell == '.':
                    self.targets.append([x, y])
                elif cell == '#':
                    self.walls.append([x, y])
        
        self.offset_x = (SCREEN_WIDTH - self.width * TILE_SIZE) // 2
        self.offset_y = (SCREEN_HEIGHT - self.height * TILE_SIZE) // 2
        self.moves = 0
    
    def is_wall(self, x, y):
        if x < 0 or y < 0 or y >= len(self.layout) or x >= len(self.layout[y]):
            return True
        return self.layout[y][x] == '#'
    
    def is_box(self, x, y):
        return [x, y] in self.boxes
    
    def move_player(self, dx, dy):
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        if self.is_wall(new_x, new_y):
            return False
        
        if self.is_box(new_x, new_y):
            box_new_x = new_x + dx
            box_new_y = new_y + dy
            
            if self.is_wall(box_new_x, box_new_y) or self.is_box(box_new_x, box_new_y):
                return False
            
            box_index = self.boxes.index([new_x, new_y])
            self.boxes[box_index] = [box_new_x, box_new_y]
        
        self.player_pos = [new_x, new_y]
        self.moves += 1
        return True
    
    def check_win(self):
        for target in self.targets:
            if target not in self.boxes:
                return False
        return True
    
    def draw(self, surface):
        surface.fill(DARK_GRAY)
        
        title = font_medium.render(LEVELS[self.level_index]["name"], True, WHITE)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 10))
        
        moves_text = font_small.render(f"Moves: {self.moves}", True, WHITE)
        surface.blit(moves_text, (10, 10))
        
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                screen_x = self.offset_x + x * TILE_SIZE
                screen_y = self.offset_y + y * TILE_SIZE
                
                pygame.draw.rect(surface, LIGHT_GRAY, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))

                # removes the visible seam/gap between adjacent '#' tiles
                if cell != '#':
                    pygame.draw.rect(surface, GRAY, (screen_x, screen_y, TILE_SIZE, TILE_SIZE), 1)
                
                if cell == '#':
                    # available, otherwise fill the entire tile with color.
                    if WALL_IMAGE:
                        surface.blit(WALL_IMAGE, (screen_x, screen_y))
                    else:
                        pygame.draw.rect(surface, BROWN, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
        
        for target in self.targets:
            screen_x = self.offset_x + target[0] * TILE_SIZE
            screen_y = self.offset_y + target[1] * TILE_SIZE
            pygame.draw.rect(surface, GREEN, (screen_x + 5, screen_y + 5, TILE_SIZE - 10, TILE_SIZE - 10), border_radius=5)
            pygame.draw.rect(surface, (50, 200, 50), (screen_x + 10, screen_y + 10, TILE_SIZE - 20, TILE_SIZE - 20), border_radius=3)
        
        for box in self.boxes:
            screen_x = self.offset_x + box[0] * TILE_SIZE
            screen_y = self.offset_y + box[1] * TILE_SIZE
            
            on_target = box in self.targets
            box_color = (255, 200, 100) if on_target else ORANGE
            
            pygame.draw.rect(surface, box_color, (screen_x + 4, screen_y + 4, TILE_SIZE - 8, TILE_SIZE - 8), border_radius=5)
            pygame.draw.rect(surface, DARK_BROWN, (screen_x + 4, screen_y + 4, TILE_SIZE - 8, TILE_SIZE - 8), 3, border_radius=5)
            pygame.draw.line(surface, DARK_BROWN, (screen_x + 10, screen_y + 10), (screen_x + TILE_SIZE - 10, screen_y + TILE_SIZE - 10), 2)
            pygame.draw.line(surface, DARK_BROWN, (screen_x + TILE_SIZE - 10, screen_y + 10), (screen_x + 10, screen_y + TILE_SIZE - 10), 2)
        
        screen_x = self.offset_x + self.player_pos[0] * TILE_SIZE
        screen_y = self.offset_y + self.player_pos[1] * TILE_SIZE
        
        pygame.draw.circle(surface, BLUE, (screen_x + TILE_SIZE // 2, screen_y + TILE_SIZE // 2), TILE_SIZE // 2 - 5)
        pygame.draw.circle(surface, CYAN, (screen_x + TILE_SIZE // 2, screen_y + TILE_SIZE // 2), TILE_SIZE // 2 - 5, 3)
        pygame.draw.circle(surface, WHITE, (screen_x + TILE_SIZE // 2 - 8, screen_y + TILE_SIZE // 2 - 5), 5)
        pygame.draw.circle(surface, WHITE, (screen_x + TILE_SIZE // 2 + 8, screen_y + TILE_SIZE // 2 - 5), 5)
        pygame.draw.circle(surface, BLACK, (screen_x + TILE_SIZE // 2 - 8, screen_y + TILE_SIZE // 2 - 5), 2)
        pygame.draw.circle(surface, BLACK, (screen_x + TILE_SIZE // 2 + 8, screen_y + TILE_SIZE // 2 - 5), 2)
        
        help_text = font_tiny.render("Arrow keys to move | R to restart | ESC for menu", True, WHITE)
        surface.blit(help_text, (SCREEN_WIDTH // 2 - help_text.get_width() // 2, SCREEN_HEIGHT - 30))

class QuizScreen:
    def __init__(self, gate_type):
        self.gate_type = gate_type
        self.question_data = random.choice(QUIZ_QUESTIONS[gate_type])
        self.selected_answer = None
        self.answered = False
        self.correct = False
        
        self.option_buttons = []
        start_y = 320
        for i, option in enumerate(self.question_data["options"]):
            btn = Button(SCREEN_WIDTH // 2 - 150, start_y + i * 70, 300, 50, option, PURPLE, CYAN)
            self.option_buttons.append(btn)
        
        self.continue_btn = Button(SCREEN_WIDTH // 2 - 100, 500, 200, 50, "Continue", GREEN, CYAN)
    
    def handle_event(self, event):
        if not self.answered:
            for i, btn in enumerate(self.option_buttons):
                if btn.handle_event(event):
                    self.selected_answer = self.question_data["options"][i]
                    self.answered = True
                    self.correct = self.selected_answer == self.question_data["answer"]
                    return None
        else:
            if self.continue_btn.handle_event(event):
                return self.correct
        return None
    
    def draw(self, surface):
        surface.fill(DARK_GRAY)
        
        title = font_large.render(f"{self.gate_type} Gate Quiz!", True, YELLOW)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        subtitle = font_small.render("Answer this question about the logic gate you just learned!", True, WHITE)
        surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 120))
        
        question_lines = self.wrap_text(self.question_data["question"], font_medium, 700)
        y = 180
        for line in question_lines:
            q_text = font_medium.render(line, True, WHITE)
            surface.blit(q_text, (SCREEN_WIDTH // 2 - q_text.get_width() // 2, y))
            y += 40
        
        if not self.answered:
            for btn in self.option_buttons:
                btn.draw(surface)
        else:
            if self.correct:
                result = font_large.render("Correct!", True, GREEN)
            else:
                result = font_large.render(f"Wrong! Answer: {self.question_data['answer']}", True, RED)
            surface.blit(result, (SCREEN_WIDTH // 2 - result.get_width() // 2, 350))
            self.continue_btn.draw(surface)
    
    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

class LessonScreen:
    def __init__(self, gate_type):
        self.gate_type = gate_type
        self.gate_info = LOGIC_GATES[gate_type]
        self.back_btn = Button(50, SCREEN_HEIGHT - 70, 150, 50, "Back", RED, ORANGE)
        self.scroll_y = 0
    
    def handle_event(self, event):
        if self.back_btn.handle_event(event):
            return "back"
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_y += event.y * 20
            self.scroll_y = min(0, self.scroll_y)
        return None
    
    def draw(self, surface):
        surface.fill(DARK_GRAY)
        
        y = 30 + self.scroll_y
        
        title = font_large.render(self.gate_info["name"], True, YELLOW)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, y))
        y += 70
        
        symbol = font_medium.render(self.gate_info["symbol"], True, CYAN)
        surface.blit(symbol, (SCREEN_WIDTH // 2 - symbol.get_width() // 2, y))
        y += 60
        
        desc_lines = self.wrap_text(self.gate_info["description"], font_small, 700)
        for line in desc_lines:
            text = font_small.render(line, True, WHITE)
            surface.blit(text, (50, y))
            y += 35
        y += 20
        
        tt_title = font_medium.render("Truth Table:", True, GREEN)
        surface.blit(tt_title, (50, y))
        y += 50
        
        table = self.gate_info["truth_table"]
        col_width = 80
        table_x = SCREEN_WIDTH // 2 - (len(table[0]) * col_width) // 2
        
        for row_idx, row in enumerate(table):
            for col_idx, cell in enumerate(row):
                cell_x = table_x + col_idx * col_width
                color = CYAN if row_idx == 0 else WHITE
                cell_text = font_small.render(cell, True, color)
                surface.blit(cell_text, (cell_x, y))
            y += 35
        y += 20
        
        real_title = font_medium.render("Real World Example:", True, ORANGE)
        surface.blit(real_title, (50, y))
        y += 45
        
        real_lines = self.wrap_text(self.gate_info["real_world"], font_small, 700)
        for line in real_lines:
            text = font_small.render(line, True, WHITE)
            surface.blit(text, (50, y))
            y += 35
        
        self.back_btn.draw(surface)
    
    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

class Game:
    def __init__(self):
        self.state = "menu"
        self.current_level = 0
        self.completed_levels = set()
        self.sokoban_game = None
        self.quiz_screen = None
        self.lesson_screen = None
        
        self.play_btn = Button(SCREEN_WIDTH // 2 - 120, 250, 240, 60, "Play", GREEN, CYAN)
        self.select_btn = Button(SCREEN_WIDTH // 2 - 120, 330, 240, 60, "Select Level", BLUE, CYAN)
        self.lessons_btn = Button(SCREEN_WIDTH // 2 - 120, 410, 240, 60, "Lessons", PURPLE, CYAN)
        
        self.level_buttons = []
        self.lesson_buttons = []
        self.back_btn = Button(50, SCREEN_HEIGHT - 70, 150, 50, "Back", RED, ORANGE)
        
        self.setup_level_buttons()
        self.setup_lesson_buttons()
        # initialize mixer for background music
        try:
            pygame.mixer.init()
        except Exception:
            pass
        self.menu_music_path = os.path.join('sounds', 'zil-sesi-433221.mp3')
        self.menu_music_playing = False
        self.prev_state = self.state
        # load right-answer sound effect if present
        self.right_answer_sound = None
        right_path = os.path.join('sounds', 'right-answer.mp3')
        try:
            if os.path.isfile(right_path):
                self.right_answer_sound = pygame.mixer.Sound(right_path)
        except Exception:
            self.right_answer_sound = None
        # load wrong-answer (buzzer) sound effect if present
        self.wrong_answer_sound = None
        wrong_path = os.path.join('sounds', 'wrong-buzzer.mp3')
        try:
            if os.path.isfile(wrong_path):
                self.wrong_answer_sound = pygame.mixer.Sound(wrong_path)
        except Exception:
            self.wrong_answer_sound = None
    
    def setup_level_buttons(self):
        self.level_buttons = []
        start_x = 100
        start_y = 180
        btn_width = 180
        btn_height = 100
        gap = 20
        cols = 3
        
        for i in range(7):
            row = i // cols
            col = i % cols
            x = start_x + col * (btn_width + gap)
            y = start_y + row * (btn_height + gap)
            btn = Button(x, y, btn_width, btn_height, f"Level {i + 1}", BLUE, CYAN)
            self.level_buttons.append(btn)
    
    def setup_lesson_buttons(self):
        self.lesson_buttons = []
        gates = ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"]
        start_x = 100
        start_y = 150
        btn_width = 180
        btn_height = 70
        gap = 15
        cols = 3
        
        for i, gate in enumerate(gates):
            row = i // cols
            col = i % cols
            x = start_x + col * (btn_width + gap)
            y = start_y + row * (btn_height + gap)
            btn = Button(x, y, btn_width, btn_height, gate, PURPLE, CYAN)
            self.lesson_buttons.append(btn)
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                self.handle_event(event)
            # handle state transitions for background music: only play in menu
            if self.prev_state != self.state:
                try:
                    # stop any currently playing music first
                    try:
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.stop()
                    except Exception:
                        pass

                    # If entering menu, loop the MP3 as background; otherwise keep music stopped
                    if self.state == 'menu':
                        if os.path.isfile(self.menu_music_path):
                            pygame.mixer.music.load(self.menu_music_path)
                            pygame.mixer.music.play(-1)
                            self.menu_music_playing = True
                        else:
                            self.menu_music_playing = False
                    else:
                        self.menu_music_playing = False
                except Exception:
                    pass
                self.prev_state = self.state

            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def handle_event(self, event):
        if self.state == "menu":
            if self.play_btn.handle_event(event):
                self.start_level(self.current_level)
            elif self.select_btn.handle_event(event):
                self.state = "level_select"
            elif self.lessons_btn.handle_event(event):
                self.state = "lessons"
        
        elif self.state == "level_select":
            if self.back_btn.handle_event(event):
                self.state = "menu"
            for i, btn in enumerate(self.level_buttons):
                if btn.handle_event(event):
                    self.start_level(i)
        
        elif self.state == "lessons":
            if self.back_btn.handle_event(event):
                self.state = "menu"
            gates = ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"]
            for i, btn in enumerate(self.lesson_buttons):
                if btn.handle_event(event):
                    self.lesson_screen = LessonScreen(gates[i])
                    self.state = "lesson_view"
        
        elif self.state == "lesson_view":
            result = self.lesson_screen.handle_event(event)
            if result == "back":
                self.state = "lessons"
        
        elif self.state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.sokoban_game.move_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.sokoban_game.move_player(0, 1)
                elif event.key == pygame.K_LEFT:
                    self.sokoban_game.move_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.sokoban_game.move_player(1, 0)
                elif event.key == pygame.K_r:
                    self.sokoban_game.load_level()
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"
                
                if self.sokoban_game.check_win():
                    self.quiz_screen = QuizScreen(self.sokoban_game.gate)
                    self.state = "quiz"
        
        elif self.state == "quiz":
            result = self.quiz_screen.handle_event(event)
            if result is not None:
                if result:
                    # play correct-answer sound if available
                    try:
                        if self.right_answer_sound:
                            self.right_answer_sound.play()
                    except Exception:
                        pass
                    self.completed_levels.add(self.current_level)
                    if self.current_level < 6:
                        self.current_level += 1
                        self.start_level(self.current_level)
                    else:
                        self.state = "victory"
                else:
                    # play wrong-answer buzzer if available
                    try:
                        if self.wrong_answer_sound:
                            self.wrong_answer_sound.play()
                    except Exception:
                        pass
                    self.start_level(self.current_level)
        
        elif self.state == "victory":
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.state = "menu"
    
    def start_level(self, level_index):
        self.current_level = level_index
        self.sokoban_game = SokobanGame(level_index)
        self.state = "playing"
    
    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "level_select":
            self.draw_level_select()
        elif self.state == "lessons":
            self.draw_lessons()
        elif self.state == "lesson_view":
            self.lesson_screen.draw(screen)
        elif self.state == "playing":
            self.sokoban_game.draw(screen)
        elif self.state == "quiz":
            self.quiz_screen.draw(screen)
        elif self.state == "victory":
            self.draw_victory()
    
    def draw_menu(self):
        screen.fill(DARK_GRAY)
        
        title = font_large.render("Logic Gates Sokoban", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
        
        subtitle = font_small.render("Learn Logic Gates Through Puzzles!", True, WHITE)
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 160))
        
        self.play_btn.draw(screen)
        self.select_btn.draw(screen)
        self.lessons_btn.draw(screen)
        
        progress = font_tiny.render(f"Completed: {len(self.completed_levels)}/7 Levels", True, GREEN)
        screen.blit(progress, (SCREEN_WIDTH // 2 - progress.get_width() // 2, 520))
    
    def draw_level_select(self):
        screen.fill(DARK_GRAY)
        
        title = font_large.render("Select Level", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        for i, btn in enumerate(self.level_buttons):
            if i in self.completed_levels:
                btn.color = GREEN
            else:
                btn.color = BLUE
            btn.draw(screen)
            
            gate = LEVELS[i]["gate"]
            gate_text = font_tiny.render(f"({gate})", True, WHITE)
            screen.blit(gate_text, (btn.rect.centerx - gate_text.get_width() // 2, btn.rect.bottom - 25))
        
        self.back_btn.draw(screen)
    
    def draw_lessons(self):
        screen.fill(DARK_GRAY)
        
        title = font_large.render("Logic Gates Lessons", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        subtitle = font_small.render("Click a gate to learn about it!", True, WHITE)
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 110))
        
        for btn in self.lesson_buttons:
            btn.draw(screen)
        
        self.back_btn.draw(screen)
    
    def draw_victory(self):
        screen.fill(DARK_GRAY)
        
        title = font_large.render("Congratulations!", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        
        message = font_medium.render("You've completed all levels!", True, GREEN)
        screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, 250))
        
        message2 = font_medium.render("You've learned about all 7 logic gates!", True, CYAN)
        screen.blit(message2, (SCREEN_WIDTH // 2 - message2.get_width() // 2, 310))
        
        continue_text = font_small.render("Click anywhere to return to menu", True, WHITE)
        screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, 420))

if __name__ == "__main__":
    game = Game()
    game.run()
