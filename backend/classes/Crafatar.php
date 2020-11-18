<?php

	// Get Crafatar from API
	class Crafatar {

		public function __construct($username,$scale) {
			$this->uuid = $this->getPlayerUUID($username);
			$this->url = "https://crafatar.com/renders/body/{$this->uuid}?scale={$scale}";

			$this->data = $this->curl();
			$this->image = imagecreatefromstring($this->data);
			$this->size = [imagesx($this->image),imagesy($this->image)];
		}
		
		// Get player UUID from username
		private function getPlayerUUID($username) {
			$url = "https://playerdb.co/api/player/minecraft/";

			$api = json_decode(file_get_contents($url.$username));
			return $api->data->player->id;
		}

		private function curl() {
			$curl = curl_init();

			curl_setopt($curl, CURLOPT_URL, $this->url); 
			curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1); // good edit, thanks!
			curl_setopt($curl, CURLOPT_BINARYTRANSFER, 1); // also, this seems wise considering output is image.

			$data = curl_exec($curl);
			curl_close($curl);

			return $data;
		}

	}