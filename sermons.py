def generate_sermon(score):
    if score >= 4:
        return ("You have shown the clarity of a calm lake. Just as Mahinda Thero saw in the king, "
                "wisdom arises when the mind is still and seeing is pure. Continue with mindfulness.")
    elif score >= 2:
        return ("The seeds of wisdom are planted. With patience and practice, the Dhamma blossoms. "
                "Reflect deeply, speak kindly, and act mindfully.")
    else:
        return ("Even a dim lamp dispels darkness. In every failure is the root of insight. "
                "Begin your path now — not in haste, but in sincerity.")
