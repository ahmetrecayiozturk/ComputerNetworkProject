import socket
from question import Question
#--------------------burası sadece server olarak çalışacaktır-----------------------
# Joker sunucusunu oluşturuyoruz
joker_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socketin ip adresini ve portunu belirliyoruz burada, localhost ip adresi ve bir kendimizin belirdiği bir portu kullanıyoruz bu genelde böyle yapılıyor
joker_socket_ip = '127.0.0.1'
joker_socket_port = 4338
#socket'in port numarasını ve ip adresini atıyoruz
joker_tcp_socket.bind((joker_socket_ip, joker_socket_port))
#5 tane bağlantı bekliyoruz o yüzden 1 yazdık
joker_tcp_socket.listen(5)

print("Joker sunucusu dinleniyor...")

questions = [
    Question("Python hangi yıl geliştirilmiştir?", "A: 1991, B: 2000, C: 1989,D: 2010", "A", "Seyirci cevabı: A:%45,B:%20,C:%35,D:%10", "Elenen cevaplar: B,C"),
    Question("Ben Hangi Yıl Doğdum?", "A: 1991 - B: 2000 - C: 2002 - D: 2010", "C", "Seyirci cevabı: A:%40,B:%25,C:%30,D:%5", "Elenen cevaplar: B,D"),
    Question("Dünya'nın uydusunun adı nedir?", "A: Mars, B: Venüs, C: Ay, D: Güneş", "C", "Seyirci cevabı: A:%5,B:%10,C:%80,D:%5", "Elenen cevaplar: A,B"),
    Question("İstanbul hangi kıtada yer alır?", "A: Avrupa, B: Asya, C: Hem Avrupa hem Asya, D: Afrika", "C", "Seyirci cevabı: A:%20,B:%15,C:%60,D:%5", "Elenen cevaplar: A,D"),
    Question("En büyük gezegen hangisidir?", "A: Mars, B: Jüpiter, C: Dünya, D: Venüs", "B", "Seyirci cevabı: A:%10,B:%70,C:%15,D:%5", "Elenen cevaplar: A,D")
]

while True:
    # gelen bağlantıyı kabul ediyoruz ve burada dönen bilgileri alıyoruz
    program_socket, program_addr = joker_tcp_socket.accept()
    print(f"Bağlantı kuruldu: {program_addr[0]}:{program_addr[1]}")

    try:
        # gelen veriyi alıyoruz
        data = program_socket.recv(1024).decode()
        print("Gelen veri:", data)
        # veriyi virgüle göre ayırıyoruz
        joket_type, question_answer, question_number = data.split(",")
        # joker türünü ve sorunun doğru cevabını alıyoruz, listede olduğu için 0 dan başlıyor bu yüzden -1 ekliyoruz
        q = questions[int(question_number) - 1]

        # joker türüne göre cevapları gönderiyoruz
        if joket_type == "S":
            joker_response = q.joker_type_s
            print("S Türü Joker cevabı:", joker_response)
            program_socket.send(joker_response.encode())
        # eğer joker türü Y ise
        elif joket_type == "Y":
            joker_response = q.joker_type_y
            print("Y Türü Joker cevabı:", joker_response)
            program_socket.send(joker_response.encode())
        # eğer joker türü geçersiz ise
        else:
            print("Geçersiz joker türü:", joket_type)
            program_socket.send("Geçersiz joker türü".encode())
    # joker sunucusuna gelen veri yoksa veya hata varsa
    except Exception as e:
        print("Hata oluştu joker sunucusunda:", e)
    # program socketini kapatıyoruz
    program_socket.close()
