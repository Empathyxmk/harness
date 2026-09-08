#include <gtest/gtest.h>
#include <string>
struct ApiSocket {
    struct Sock {
        int send(const std::string& d) { return 5; }
        std::string receive(int) { return "hello"; }
    };
    Sock* socket;
    ApiSocket(Sock* s): socket(s){}
    int send(const std::string& d) { return socket->send(d);}
    std::string receive(int n) { return socket->receive(n);}
};
TEST(TestSocketPublic, test_socket_send_and_receive) {
    ApiSocket::Sock s;
    ApiSocket sock(&s);
    EXPECT_EQ(sock.send("hello"), 5);
    EXPECT_EQ(sock.receive(5), "hello");
}