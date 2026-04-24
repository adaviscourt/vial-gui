# SPDX-License-Identifier: GPL-2.0-or-later
import unittest

from protocol.dummy_keyboard import DummyKeyboard
from keycodes.keycodes import Keycode, recreate_keyboard_keycodes
from macro.macro_action import ActionTap, ActionDown, ActionText, ActionDelay, ActionUp
from macro.macro_key import KeyDown, KeyTap, KeyUp, KeyString
from macro.macro_optimizer import remove_repeats, replace_with_tap, replace_with_string

KC_A = Keycode.find_by_qmk_id("KC_A")
KC_B = Keycode.find_by_qmk_id("KC_B")
KC_C = Keycode.find_by_qmk_id("KC_C")

CMB_TOG = Keycode.find_by_qmk_id("CMB_TOG")


class TestMacro(unittest.TestCase):

    def test_remove_repeats(self):
        self.assertEqual(remove_repeats([KeyDown(KC_A), KeyDown(KC_A)]), [KeyDown(KC_A)])
        self.assertEqual(remove_repeats([KeyDown(KC_A), KeyDown(KC_B), KeyDown(KC_B), KeyDown(KC_C), KeyDown(KC_C)]),
                         [KeyDown(KC_A), KeyDown(KC_B), KeyDown(KC_C)])

        # don't remove repeated taps
        self.assertEqual(remove_repeats([KeyTap(KC_A), KeyTap(KC_A)]), [KeyTap(KC_A), KeyTap(KC_A)])

    def test_replace_tap(self):
        self.assertEqual(replace_with_tap([KeyDown(KC_A)]), [KeyDown(KC_A)])
        self.assertEqual(replace_with_tap([KeyDown(KC_A), KeyUp(KC_A)]), [KeyTap(KC_A)])
        self.assertEqual(replace_with_tap([KeyUp(KC_A), KeyDown(KC_A)]), [KeyUp(KC_A), KeyDown(KC_A)])

    def test_replace_string(self):
        self.assertEqual(replace_with_string([KeyTap(KC_A), KeyTap(KC_B)]), [KeyString("ab")])

    def test_serialize_v1(self):
        kb = DummyKeyboard(None)
        kb.vial_protocol = 1
        data = kb.macro_serialize([ActionText("Hello"), ActionTap(["KC_A", "KC_B", "KC_C"]), ActionText("World"),
                                   ActionDown(["KC_C", "KC_B", "KC_A"])])
        self.assertEqual(data, b"Hello\x01\x04\x01\x05\x01\x06World\x02\x06\x02\x05\x02\x04")

    def test_deserialize_v1(self):
        kb = DummyKeyboard(None)
        kb.vial_protocol = 1
        macro = kb.macro_deserialize(b"Hello\x01\x04\x01\x05\x01\x06World\x02\x06\x02\x05\x02\x04")
        self.assertEqual(macro, [ActionText("Hello"), ActionTap(["KC_A", "KC_B", "KC_C"]), ActionText("World"),
                                 ActionDown(["KC_C", "KC_B", "KC_A"])])

    def test_serialize_v2(self):
        kb = DummyKeyboard(None)
        kb.vial_protocol = 2
        data = kb.macro_serialize([ActionText("Hello"), ActionTap(["KC_A", "KC_B", "KC_C"]), ActionText("World"),
                                   ActionDown(["KC_C", "KC_B", "KC_A"]), ActionDelay(1000)])
        self.assertEqual(data, b"Hello\x01\x01\x04\x01\x01\x05\x01\x01\x06World\x01\x02\x06\x01\x02\x05\x01\x02\x04"
                               b"\x01\x04\xEC\x04")
        data = kb.macro_serialize([ActionText("Hello"), ActionTap(["KC_A", "KC_B", "KC_C"]), ActionText("World"),
                                   ActionDown(["KC_C", "KC_B", "KC_A"]), ActionDelay(0)])
        self.assertEqual(data, b"Hello\x01\x01\x04\x01\x01\x05\x01\x01\x06World\x01\x02\x06\x01\x02\x05\x01\x02\x04"
                               b"\x01\x04\x01\x01")
        data = kb.macro_serialize([ActionText("Hello"), ActionTap(["KC_A", "KC_B", "KC_C"]), ActionText("World"),
                                   ActionDown(["KC_C", "KC_B", "KC_A"]), ActionDelay(1)])
        self.assertEqual(data, b"Hello\x01\x01\x04\x01\x01\x05\x01\x01\x06World\x01\x02\x06\x01\x02\x05\x01\x02\x04"
                               b"\x01\x04\x02\x01")
        data = kb.macro_serialize([ActionText("Hello"), ActionTap(["KC_A", "KC_B", "KC_C"]), ActionText("World"),
                                   ActionDown(["KC_C", "KC_B", "KC_A"]), ActionDelay(256)])
        self.assertEqual(data, b"Hello\x01\x01\x04\x01\x01\x05\x01\x01\x06World\x01\x02\x06\x01\x02\x05\x01\x02\x04"
                               b"\x01\x04\x02\x02")

    def test_deserialize_v2(self):
        kb = DummyKeyboard(None)
        kb.vial_protocol = 2
        macro = kb.macro_deserialize(b"Hello\x01\x01\x04\x01\x01\x05\x01\x01\x06World\x01\x02\x06\x01\x02\x05"
                                     b"\x01\x02\x04\x01\x04\xEC\x04")
        self.assertEqual(macro, [ActionText("Hello"), ActionTap(["KC_A", "KC_B", "KC_C"]), ActionText("World"),
                                 ActionDown(["KC_C", "KC_B", "KC_A"]), ActionDelay(1000)])
        macro = kb.macro_deserialize(b"Hello\x01\x01\x04\x01\x01\x05\x01\x01\x06World\x01\x02\x06\x01\x02\x05"
                                     b"\x01\x02\x04\x01\x04\x01\x01")
        self.assertEqual(macro, [ActionText("Hello"), ActionTap(["KC_A", "KC_B", "KC_C"]), ActionText("World"),
                                 ActionDown(["KC_C", "KC_B", "KC_A"]), ActionDelay(0)])
        macro = kb.macro_deserialize(b"Hello\x01\x01\x04\x01\x01\x05\x01\x01\x06World\x01\x02\x06\x01\x02\x05"
                                     b"\x01\x02\x04\x01\x04\x02\x01")
        self.assertEqual(macro, [ActionText("Hello"), ActionTap(["KC_A", "KC_B", "KC_C"]), ActionText("World"),
                                 ActionDown(["KC_C", "KC_B", "KC_A"]), ActionDelay(1)])
        macro = kb.macro_deserialize(b"Hello\x01\x01\x04\x01\x01\x05\x01\x01\x06World\x01\x02\x06\x01\x02\x05"
                                     b"\x01\x02\x04\x01\x04\x02\x02")
        self.assertEqual(macro, [ActionText("Hello"), ActionTap(["KC_A", "KC_B", "KC_C"]), ActionText("World"),
                                 ActionDown(["KC_C", "KC_B", "KC_A"]), ActionDelay(256)])

    def test_save(self):
        down = ActionDown(["KC_A", "KC_B", "CMB_TOG"])
        self.assertEqual(down.save(), ["down", "KC_A", "KC_B", "CMB_TOG"])
        tap = ActionTap(["CMB_TOG", "KC_B", "KC_A"])
        self.assertEqual(tap.save(), ["tap", "CMB_TOG", "KC_B", "KC_A"])
        text = ActionText("Hello world")
        self.assertEqual(text.save(), ["text", "Hello world", 0])
        text = ActionText("Hello world", 25)
        self.assertEqual(text.save(), ["text", "Hello world", 25])
        delay = ActionDelay(123)
        self.assertEqual(delay.save(), ["delay", 123])

    def test_restore(self):
        down = ActionDown()
        down.restore(["down", "KC_A", "KC_B", "CMB_TOG"])
        self.assertEqual(down, ActionDown(["KC_A", "KC_B", "CMB_TOG"]))
        tap = ActionTap()
        tap.restore(["tap", "CMB_TOG", "KC_B", "KC_A"])
        self.assertEqual(tap, ActionTap(["CMB_TOG", "KC_B", "KC_A"]))
        # legacy save format without char_delay must still restore
        text = ActionText()
        text.restore(["text", "Hello world"])
        self.assertEqual(text, ActionText("Hello world"))
        # new save format with char_delay
        text = ActionText()
        text.restore(["text", "Hello world", 25])
        self.assertEqual(text, ActionText("Hello world", 25))
        delay = ActionDelay()
        delay.restore(["delay", 123])
        self.assertEqual(delay, ActionDelay(123))

    def test_serialize_text_char_delay(self):
        kb = DummyKeyboard(None)
        kb.vial_protocol = 2
        # delay=1 -> per-char bytes: \x01\x04\x02\x01 (SS_QMK_PREFIX, SS_DELAY_CODE, 2, 1)
        data = kb.macro_serialize([ActionText("abc", 1)])
        self.assertEqual(data, b"a\x01\x04\x02\x01b\x01\x04\x02\x01c")
        # empty text produces no bytes
        data = kb.macro_serialize([ActionText("", 50)])
        self.assertEqual(data, b"")
        # single char produces no trailing delay
        data = kb.macro_serialize([ActionText("x", 50)])
        self.assertEqual(data, b"x")
        # char_delay=0 preserves legacy single-blob behavior
        data = kb.macro_serialize([ActionText("abc", 0)])
        self.assertEqual(data, b"abc")

    def test_serialize_text_char_delay_v1_raises(self):
        kb = DummyKeyboard(None)
        kb.vial_protocol = 1
        # char_delay requires protocol v2 (same policy as ActionDelay)
        with self.assertRaises(RuntimeError):
            kb.macro_serialize([ActionText("abc", 10)])
        # char_delay=0 on v1 still works (unchanged behavior)
        data = kb.macro_serialize([ActionText("abc", 0)])
        self.assertEqual(data, b"abc")

    def test_twobyte_keycodes(self):
        kb = DummyKeyboard(None)
        kb.vial_protocol = 2
        # TODO remove once keycodes are properly owned by the Keyboard object
        kb.tap_dance_count = 0
        recreate_keyboard_keycodes(kb)

        data = kb.macro_serialize([ActionTap(["CMB_TOG", "KC_A"])])
        self.assertEqual(data, b"\x01\x05\xF9\x5C\x01\x01\x04")
        data = kb.macro_serialize([ActionDown(["CMB_TOG", "KC_A"])])
        self.assertEqual(data, b"\x01\x06\xF9\x5C\x01\x02\x04")
        data = kb.macro_serialize([ActionUp(["CMB_TOG", "KC_A"])])
        self.assertEqual(data, b"\x01\x07\xF9\x5C\x01\x03\x04")

        macro = kb.macro_deserialize(b"\x01\x05\xF9\x5C\x01\x01\x04")
        self.assertEqual(macro, [ActionTap(["CMB_TOG", "KC_A"])])
        macro = kb.macro_deserialize(b"\x01\x06\xF9\x5C\x01\x02\x04")
        self.assertEqual(macro, [ActionDown(["CMB_TOG", "KC_A"])])
        macro = kb.macro_deserialize(b"\x01\x07\xF9\x5C\x01\x03\x04")
        self.assertEqual(macro, [ActionUp(["CMB_TOG", "KC_A"])])

    def test_twobyte_with_zeroes(self):
        kb = DummyKeyboard(None)
        kb.vial_protocol = 2
        data = kb.macro_serialize([ActionTap([Keycode.serialize(0xA000), Keycode.serialize(0xB100), Keycode.serialize(0xC200)])])
        self.assertEqual(data, b"\x01\x05\xA0\xFF\x01\x05\xB1\xFF\x01\x05\xC2\xFF")

        macro = kb.macro_deserialize(b"\x01\x05\xC2\xFF\x01\x05\xB1\xFF\x01\x05\xA0\xFF")
        self.assertEqual(macro, [ActionTap([Keycode.serialize(0xC200), Keycode.serialize(0xB100), Keycode.serialize(0xA000)])])
