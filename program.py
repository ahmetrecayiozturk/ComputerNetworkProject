import socket
from question import Question
#-----------------------server tarafı------------------------
#önce server'a ait tcp socket oluşturuyoruz
program_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socketin ip adresini ve portunu belirliyoruz burada, localhost ip adresi ve bir kendimizin belirdiği bir portu kullanıyoruz bu genelde böyle yapılıyor
program_ip= '127.0.0.1'
program_port = 4337
#socket'in port numarasını ve ip adresini atıyoruz
program_tcp_socket.bind((program_ip, program_port))
#sadece bir tane yarışmacı bağlantısı bekliyoruz
program_tcp_socket.listen(1)
#competition_socket ve competition_addr değişkenlerine gelen bağlantıyı kabul ediyoruz ve bu değişkenlere bağlantıyı atıyoruz, bu bağlanan kişinin yani yarışmacının adresini ve socketini tutar
competition_socket, competition_addr = program_tcp_socket.accept()
#burada istemcinin ip adresini ve portunu yazdırıyoruz(kontrol amaçlı)
print(f"Bağlantı kuruldu: {competition_addr[0]}:{competition_addr[1]}")
#şimdi de istemciden gelen bilgiyi yani mesajı alalım bakalım
data = competition_socket.recv(1024).decode()
#burada istemciden gelen veriyi yazdırıyoruz
print("Gelen veri:", data)
#-------------------------Soruların yazılması----------------------------------------------
# Sorular
questions = [
    Question("Python hangi yıl geliştirilmiştir?", "A: 1991, B: 2000, C: 1989,D: 2010", "A", "Seyirci cevabı: A:%45,B:%20,C:%35,D:%10", "Elenen cevaplar: B,C"),
    Question("Ben Hangi Yıl Doğdum?", "A: 1991 - B: 2000 - C: 2002 - D: 2010", "C", "Seyirci cevabı: A:%40,B:%25,C:%30,D:%5", "Elenen cevaplar: B,D"),
    Question("Dünya'nın uydusunun adı nedir?", "A: Mars, B: Venüs, C: Ay, D: Güneş", "C", "Seyirci cevabı: A:%5,B:%10,C:%80,D:%5", "Elenen cevaplar: A,B"),
    Question("İstanbul hangi kıtada yer alır?", "A: Avrupa, B: Asya, C: Hem Avrupa hem Asya, D: Afrika", "C", "Seyirci cevabı: A:%20,B:%15,C:%60,D:%5", "Elenen cevaplar: A,D"),
    Question("En büyük gezegen hangisidir?", "A: Mars, B: Jüpiter, C: Dünya, D: Venüs", "B", "Seyirci cevabı: A:%10,B:%70,C:%15,D:%5", "Elenen cevaplar: A,D")
]
odul_tablosu = {
    0: "Linç Yükleniyor",
    1: "Önemli olan katılmaktı",
    2: "İki birden büyüktür",
    3: "Buralara kolay gelmedik",
    4: "Sen bu işi biliyorsun",
    5: "Harikasın"
}
#-------------------------yarışmanın başlaması--------------------------

dogru_sayisi = 0  # Doğru cevap sayacı

# Yarışma döngüsü
for question in questions:
    # Soruyu ve seçenekleri gönder
    competition_socket.send(f"{question.question}\n{question.options}\n".encode())
    # Joker tekrar kullanımına izin vermek için döngü kullanıyoruz
    while True:
        # Sorudan gelen cevabı al
        data = competition_socket.recv(1024).decode().strip().upper()
        # Eğer joker kullanmak istiyorsa
        if data == "S" or data == "Y":
            # önce bağlanılacak tcp socket oluşturuyoruz
            joker_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # socketin ip adresini ve portunu belirliyoruz burada, localhost ip adresi ve bir kendimizin belirdiği bir portu kullanıyoruz bu genelde böyle yapılıyor
            joker_socket_ip = '127.0.0.1'
            joker_socket_port = 4338
            # burada joker sunucusuna bağlanıyoruz
            joker_tcp_socket.connect((joker_socket_ip, joker_socket_port))
            # burada joker sunucusuna mesaj gönderiyoruz mesajımız ise yarışmacının joker kullanmak istediği hangi joker ise o gidiyor
            joker_tcp_socket.send(f"{data},{question.correct_answer},{questions.index(question) + 1}".encode())
            # joker cevabını alıyoruz
            joker_data = joker_tcp_socket.recv(1024).decode()
            # joker cevabını yarışmacıya gönderiyoruz
            competition_socket.send(f"JOKER CEVABI: {joker_data}\nCevabınızı tekrar girin: ".encode())
            # bağlantıyı kapatıyoruz
            joker_tcp_socket.close()
            continue  # cevaba geçmeden tekrar veri bekleniyor
        else:
            break  # gerçek cevap girilmişse döngüden çık
    # Cevap doğruysa
    if data == question.correct_answer:
        dogru_sayisi += 1
        if dogru_sayisi == len(questions):  # Son soruyu da doğru bildiyse
            odul = odul_tablosu[dogru_sayisi]
            competition_socket.send(
                f"Tebrikler! Doğru cevap verdiniz.\nYarışma bitti! Tüm soruları doğru bildiniz!\nÖdülünüz: {odul}\n".encode())
        else:
            competition_socket.send(f"Tebrikler! Doğru cevap verdiniz.\n".encode())
    # Cevap yanlışsa
    else:
        odul = odul_tablosu[dogru_sayisi]
        competition_socket.send(
            f"Yanlış cevap verdiniz. Doğru cevap: {question.correct_answer}\nYarışma sona erdi.\nÖdülünüz: {odul}\n".encode())
        break

    print("Verilen Cevap: ", data)
