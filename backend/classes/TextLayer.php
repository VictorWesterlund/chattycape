<?php

	// Add horizontally centered text at x,y
	class TextLayer {

		public function __construct($text,$font,$size) {
			$this->text = $text;
			$this->font = $font;

			$this->size = $this->scaleFont($text,$size);
			$this->setFontPath();
		}

		// Prevent default GD font lookup path from being used
		private function setFontPath() {
			putenv("GDFONTPATH=".realpath("./".$this->font));
		}

		// Calculate scaled front size from max-width
		private function scaleFont($text,$baseline) {
			$len = strlen($this->text);

			$log = $len / 0.6;
			$size = $baseline - $log;

			return $size;
		}

		// Center text
		private function offsetX($x) {
			$len = strlen($this->text);

			$offset = $x - ($len * ($this->size / 2.2));

			return $offset;
		}

		// Image resource, x, y
		public function textcopy($image,$x,$y,$color) {
			imagettftext($image,$this->size,0,$this->offsetX($x),$y,$color,"font",$this->text);
			return true;
		}

	}