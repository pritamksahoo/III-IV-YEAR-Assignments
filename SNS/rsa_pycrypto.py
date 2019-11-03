from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

pass_code = "leomessi"

def rsa_keygen():
	'''Generate an RSA key and store it
	in a binary file encrypted by a pass-code
	'''

	key = RSA.generate(2048)

	# Private part of the key
	try:
		enc_pvt_key = key.exportKey('PEM', passphrase=pass_code, pkcs=1)

		pvt_file = open("private.pem", "wb")
		pvt_file.write(enc_pvt_key)

	except Exception as e:
		print(e)

	# Public part of the key
	try:
		enc_pub_key = key.publickey().exportKey('PEM', passphrase=pass_code)

		pub_file = open("public.pem", "wb")
		pub_file.write(enc_pub_key)

	except Exception as e:
		print(e)

	'''END'''


def encrypt(message):
	'''
	Encrypt a message using generated public key
	'''
	# Converting string into bytes
	message = message.encode("utf-8")

	try:
		# Import the public key
		pub_key = RSA.importKey(open("public.pem", 'rb').read(), passphrase=pass_code)
		# Encryption
		enc_msg = pub_key.encrypt(message, 32)[0]

		enc_msg_file = open("encrypted_message.bin", "wb")
		enc_msg_file.write(enc_msg)

	except Exception as e:
		print(e)

	'''END'''


def decrypt():
	'''
	Decrypt an encrypted message using generated private key
	'''
	try:
		# Import the private key
		pvt_key = RSA.importKey(open("private.pem", 'rb').read(), passphrase=pass_code)
		# Read the encrypted message
		enc_msg = open("encrypted_message.bin", "rb").read()
		# Decryption
		dec_msg = pvt_key.decrypt(enc_msg)

		dec_msg_file = open("decrypted_message.bin", "wb")
		dec_msg_file.write(dec_msg)

	except Exception as e:
		print(e)

	'''END'''


def read_msg(filename, mode):
	'''Read a binary file'''
	content = open(filename, "rb").read()

	if mode == 'dec':
		content = content.decode('utf-8')

	print(content)
	'''END'''

if __name__ == '__main__':
	rsa_keygen()

	message = "Two wrongs don't make a right"
	print("\nGiven message :", message)

	# Encryption
	encrypt(message)
	print("\nEncrypted message : ", end='')
	read_msg("encrypted_message.bin", 'enc')

	# Decryption
	decrypt()
	print("\nDecrypted message : ", end='')
	read_msg("decrypted_message.bin", 'dec')

	print()
	'''END'''