import math
import gradio as gr


def create_calculator():
    with gr.Blocks(title="Scientific Calculator") as demo:

        # Declare non-rendering state components at top level
        equation = gr.State(value="", render=False)
        history_list = gr.State(value=[], render=False)
        angle_mode = gr.State(value="Rad", render=False)

        gr.Markdown("### 🔬 Scientific Engineering Calculator")

        with gr.Row():
            with gr.Column(scale=3):
                # Configuration & Display row
                with gr.Row():
                    mode_display = gr.Textbox(
                        value="Mode: Rad",
                        label="Unit",
                        interactive=False,
                        scale=1,
                    )
                    display = gr.Textbox(
                        value="",
                        label="Display",
                        interactive=False,
                        text_align="right",
                        scale=4,
                    )

                # Top Functional Row
                with gr.Row():
                    btn_ac = gr.Button("AC", variant="stop")
                    btn_c = gr.Button("C", variant="stop")
                    btn_mode = gr.Button("Rad/Deg", variant="secondary")
                    btn_paren_open = gr.Button("(", variant="secondary")
                    btn_paren_close = gr.Button(")", variant="secondary")

                # Scientific Layout Row 1 (Trigonometry)
                with gr.Row():
                    btn_sin = gr.Button("sin", variant="secondary")
                    btn_cos = gr.Button("cos", variant="secondary")
                    btn_tan = gr.Button("tan", variant="secondary")
                    btn_asin = gr.Button("sin⁻¹", variant="secondary")
                    btn_acos = gr.Button("cos⁻¹", variant="secondary")
                    btn_atan = gr.Button("tan⁻¹", variant="secondary")

                # Scientific Layout Row 2 (Logs, Exponents, Roots)
                with gr.Row():
                    btn_ln = gr.Button("ln", variant="secondary")
                    btn_log = gr.Button("log", variant="secondary")
                    btn_pow = gr.Button("x^y", variant="secondary")
                    btn_sqrt = gr.Button("√", variant="secondary")
                    btn_inv = gr.Button("1/x", variant="secondary")
                    btn_fact = gr.Button("x!", variant="secondary")

                # Core Numpad Mapping
                numpad = [
                    ["7", "8", "9", "/", "%"],
                    ["4", "5", "6", "*", "π"],
                    ["1", "2", "3", "-", "⌫"],
                    ["0", ".", "=", "+", ""],
                ]

                btn_map = {}
                for row in numpad:
                    with gr.Row():
                        for char in row:
                            if char == "":
                                continue
                            is_num = char.isdigit() or char == "."
                            is_eval = char == "="
                            variant = (
                                "primary"
                                if is_eval
                                else "secondary" if not is_num else "default"
                            )

                            btn = gr.Button(char, variant=variant)
                            btn_map[char] = btn

            # Side Panel: History Log
            with gr.Column(scale=1):
                gr.Markdown("#### 📜 Calculation History")
                history_display = gr.TextArea(
                    value="No history yet.",
                    max_lines=15,
                    interactive=False,
                    show_label=False,
                )
                btn_clear_hist = gr.Button(
                    "Clear History", variant="stop", size="sm"
                )

        # --- Operational Logic Functions ---

        def toggle_angle_mode(current_mode):
            next_mode = "Deg" if current_mode == "Rad" else "Rad"
            return next_mode, f"Mode: {next_mode}"

        def add_char(char, current_eq):
            mapping = {"x^y": "^", "x!": "!"}
            char_to_add = mapping.get(char, char)

            operators = ["+", "-", "*", "/", ".", "^", "%"]
            if (
                char_to_add in operators
                and current_eq
                and current_eq[-1] in operators
            ):
                return current_eq, current_eq

            new_eq = current_eq + str(char_to_add)
            return new_eq, new_eq

        def backspace(current_eq):
            return current_eq[:-1], current_eq[:-1]

        def clear_all():
            return "", ""

        def clear_entry(current_eq):
            operators = ["+", "-", "*", "/", "^", "%", "(", ")"]
            if not current_eq:
                return "", ""

            indices = [
                current_eq.rfind(op)
                for op in operators
                if current_eq.rfind(op) != -1
            ]
            if not indices:
                return "", ""

            cut_idx = max(indices) + 1
            new_eq = current_eq[:cut_idx]
            return new_eq, new_eq

        # --- Scientific Calculation Engine ---
        def run_scientific_eval(func_name, current_eq, mode):
            try:
                if not current_eq.strip():
                    return "", ""
                val = float(
                    eval(current_eq.replace("^", "**").replace("π", str(math.pi)))
                )

                if func_name == "sin":
                    res = math.sin(math.radians(val) if mode == "Deg" else val)
                elif func_name == "cos":
                    res = math.cos(math.radians(val) if mode == "Deg" else val)
                elif func_name == "tan":
                    res = math.tan(math.radians(val) if mode == "Deg" else val)
                elif func_name == "asin":
                    if not -1 <= val <= 1:
                        return "Domain Error", ""
                    res = (
                        math.degrees(math.asin(val))
                        if mode == "Deg"
                        else math.asin(val)
                    )
                elif func_name == "acos":
                    if not -1 <= val <= 1:
                        return "Domain Error", ""
                    res = (
                        math.degrees(math.acos(val))
                        if mode == "Deg"
                        else math.acos(val)
                    )
                elif func_name == "atan":
                    res = (
                        math.degrees(math.atan(val))
                        if mode == "Deg"
                        else math.atan(val)
                    )
                elif func_name == "ln":
                    if val <= 0:
                        return "Domain Error", ""
                    res = math.log(val)
                elif func_name == "log":
                    if val <= 0:
                        return "Domain Error", ""
                    res = math.log10(val)
                elif func_name == "sqrt":
                    if val < 0:
                        return "Domain Error", ""
                    res = math.sqrt(val)
                elif func_name == "inv":
                    if val == 0:
                        return "Cannot divide by 0", ""
                    res = 1 / val
                elif func_name == "fact":
                    if val < 0 or not val.is_integer():
                        return "Invalid Input", ""
                    res = math.factorial(int(val))

                formatted = f"{res:g}"
                return formatted, formatted
            except Exception:
                return "Error", ""

        # --- Core Mathematical Evaluation & History Logger ---
        def execute_calculation(current_eq, structural_history):
            if not current_eq.strip():
                return (
                    "",
                    "",
                    "\n".join(structural_history)
                    if structural_history
                    else "No history yet.",
                )

            try:
                processed = current_eq.replace("^", "**").replace(
                    "π", str(math.pi)
                )

                if "/0" in processed:
                    return (
                        "Cannot divide by 0",
                        "",
                        "\n".join(structural_history),
                    )

                result_raw = eval(processed)
                formatted_result = f"{result_raw:g}"

                record = f"{current_eq} = {formatted_result}"
                structural_history.append(record)
                history_text = "\n".join(structural_history)

                return formatted_result, formatted_result, history_text
            except Exception:
                return "Syntax Error", "", "\n".join(structural_history)

        def clear_history_stack():
            return [], "No history yet."

        # --- UI Wire Binding Config ---
        btn_mode.click(
            fn=toggle_angle_mode,
            inputs=[angle_mode],
            outputs=[angle_mode, mode_display],
        )
        btn_ac.click(fn=clear_all, outputs=[display, equation])
        btn_c.click(
            fn=clear_entry, inputs=[equation], outputs=[display, equation]
        )
        btn_clear_hist.click(
            fn=clear_history_stack, outputs=[history_list, history_display]
        )

        for char, btn_obj in btn_map.items():
            if char == "=":
                btn_obj.click(
                    fn=execute_calculation,
                    inputs=[equation, history_list],
                    outputs=[display, equation, history_display],
                )
            elif char == "⌫":
                btn_obj.click(
                    fn=backspace,
                    inputs=[equation],
                    outputs=[display, equation],
                )
            else:
                btn_obj.click(
                    fn=add_char,
                    inputs=[gr.State(char), equation],
                    outputs=[display, equation],
                )

        btn_paren_open.click(
            fn=add_char,
            inputs=[gr.State("("), equation],
            outputs=[display, equation],
        )
        btn_paren_close.click(
            fn=add_char,
            inputs=[gr.State(")"), equation],
            outputs=[display, equation],
        )
        btn_pow.click(
            fn=add_char,
            inputs=[gr.State("x^y"), equation],
            outputs=[display, equation],
        )
        btn_fact.click(
            fn=add_char,
            inputs=[gr.State("x!"), equation],
            outputs=[display, equation],
        )

        sc_buttons = {
            btn_sin: "sin",
            btn_cos: "cos",
            btn_tan: "tan",
            btn_asin: "asin",
            btn_acos: "acos",
            btn_atan: "atan",
            btn_ln: "ln",
            btn_log: "log",
            btn_sqrt: "sqrt",
            btn_inv: "inv",
        }

        for btn_obj, func_identifier in sc_buttons.items():
            btn_obj.click(
                fn=run_scientific_eval,
                inputs=[gr.State(func_identifier), equation, angle_mode],
                outputs=[display, equation],
            )

        return demo

if __name__ == "__main__":
    app = create_calculator()
    app.launch(share=True)