import pyray as pr
from blockchain.blockchain import Blockchain

# Skapa test-chain
chain = Blockchain()
chain.add_block({"action": "Fix bug"})
chain.add_block({"action": "Write report"})
chain.add_block({"action": "Deploy app"})

pr.init_window(1000, 600, "Blockchain Visualizer")
pr.set_target_fps(60)

BLOCK_WIDTH = 180
BLOCK_HEIGHT = 100
MARGIN = 40

while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)

    x = MARGIN
    y = 250

    is_valid = chain.is_chain_valid()

    for i, block in enumerate(chain.chain):

        # Färg
        color = pr.GREEN if is_valid else pr.RED

        # Rita block
        pr.draw_rectangle(x, y, BLOCK_WIDTH, BLOCK_HEIGHT, color)
        pr.draw_rectangle_lines(x, y, BLOCK_WIDTH, BLOCK_HEIGHT, pr.BLACK)

        # Text
        pr.draw_text(f"Index: {block.index}", x+10, y+10, 16, pr.BLACK)

        preview = str(block.data)
        if len(preview) > 20:
            preview = preview[:20] + "..."

        pr.draw_text(preview, x+10, y+40, 14, pr.BLACK)
        pr.draw_text(block.hash[:10], x+10, y+70, 12, pr.DARKGRAY)

        # Linje till nästa block
        if i < len(chain.chain) - 1:
            pr.draw_line(
                x + BLOCK_WIDTH,
                y + BLOCK_HEIGHT // 2,
                x + BLOCK_WIDTH + MARGIN,
                y + BLOCK_HEIGHT // 2,
                pr.BLACK
            )

        x += BLOCK_WIDTH + MARGIN

    pr.draw_text(
        "VALID" if is_valid else "INVALID",
        20, 20, 30,
        pr.GREEN if is_valid else pr.RED
    )

    pr.end_drawing()

pr.close_window()