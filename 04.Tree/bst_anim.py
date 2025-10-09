from manim import *


class BSTNode:
    """二分探索木のノードクラス"""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTreeConstruction(Scene):
    def construct(self):
        # タイトル
        title = Text("二分探索木の構築", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 挿入する値のリスト
        values = [50, 30, 70, 20, 40, 60, 80]

        # 値の表示
        values_text = Text(f"挿入する値: {values}", font_size=24)
        values_text.next_to(title, DOWN)
        self.play(Write(values_text))
        self.wait(1)

        # 木のルート初期化
        self.tree_root = None
        self.node_objects = {}  # 値 -> (circle, text) のマッピング
        self.edge_objects = []  # エッジのリスト

        # 各値を順次挿入
        for i, value in enumerate(values):
            # 現在挿入する値をハイライト
            highlight = Text(f"挿入: {value}", font_size=28, color=YELLOW)
            highlight.next_to(values_text, DOWN)
            self.play(Write(highlight))

            # 挿入アニメーション
            self.insert_with_animation(value)

            self.play(FadeOut(highlight))
            self.wait(0.5)

        # 最終メッセージ
        final_text = Text("構築完了！", font_size=32, color=GREEN)
        final_text.to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(2)

    def insert_with_animation(self, value):
        """値を二分探索木に挿入し、アニメーション表示"""
        if self.tree_root is None:
            # ルートノードの作成
            self.tree_root = BSTNode(value)
            circle, text = self.create_node_visual(value, ORIGIN)
            self.node_objects[value] = (circle, text)
            self.play(Create(circle), Write(text))
        else:
            # 挿入位置を探索
            path = self.find_insert_path(self.tree_root, value)
            self.animate_search_path(path, value)

            # 新しいノードを挿入
            parent = path[-1]
            new_node = BSTNode(value)

            # 親ノードの左右どちらに挿入するか決定
            if value < parent.value:
                parent.left = new_node
                position = self.calculate_position(parent.value, "left")
            else:
                parent.right = new_node
                position = self.calculate_position(parent.value, "right")

            # 新しいノードの視覚要素を作成
            circle, text = self.create_node_visual(value, position)
            self.node_objects[value] = (circle, text)

            # エッジの作成
            parent_circle = self.node_objects[parent.value][0]
            edge = Line(parent_circle.get_center(), circle.get_center(), color=WHITE)
            self.edge_objects.append(edge)

            # アニメーション
            self.play(Create(edge))
            self.play(Create(circle), Write(text))

    def find_insert_path(self, node, value):
        """挿入位置までのパスを返す"""
        path = []
        current = node
        while current:
            path.append(current)
            if value < current.value:
                if current.left is None:
                    break
                current = current.left
            else:
                if current.right is None:
                    break
                current = current.right
        return path

    def animate_search_path(self, path, value):
        """探索パスをアニメーション表示"""
        for node in path:
            circle, text = self.node_objects[node.value]
            # ノードを一時的にハイライト
            self.play(circle.animate.set_fill(YELLOW, opacity=0.3), run_time=0.3)
            self.play(circle.animate.set_fill(BLUE, opacity=0), run_time=0.3)

    def create_node_visual(self, value, position):
        """ノードの視覚要素（円とテキスト）を作成"""
        circle = Circle(radius=0.4, color=BLUE, fill_opacity=0)
        circle.move_to(position)

        text = Text(str(value), font_size=28)
        text.move_to(circle.get_center())

        return circle, text

    def calculate_position(self, parent_value, direction):
        """親ノードから子ノードの位置を計算"""
        parent_circle = self.node_objects[parent_value][0]
        parent_pos = parent_circle.get_center()

        # 深さに応じて横方向の間隔を調整
        depth = self.get_depth(self.tree_root, parent_value)
        horizontal_spacing = 2.0 / (2**depth)
        vertical_spacing = 1.2

        if direction == "left":
            new_pos = parent_pos + LEFT * horizontal_spacing + DOWN * vertical_spacing
        else:
            new_pos = parent_pos + RIGHT * horizontal_spacing + DOWN * vertical_spacing

        return new_pos

    def get_depth(self, node, target_value, current_depth=0):
        """指定された値のノードの深さを取得"""
        if node is None:
            return -1
        if node.value == target_value:
            return current_depth

        left_depth = self.get_depth(node.left, target_value, current_depth + 1)
        if left_depth != -1:
            return left_depth

        return self.get_depth(node.right, target_value, current_depth + 1)


# 実行コマンド:
# manim -pql このファイル名.py BinarySearchTreeConstruction
#
# オプション説明:
# -p: 完成後に自動再生
# -q: 品質設定 (l=low, m=medium, h=high, k=4k)
#
# 高品質版: manim -pqh このファイル名.py BinarySearchTreeConstruction
