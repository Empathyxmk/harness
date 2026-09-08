#include <gtest/gtest.h>
#include "pdf_redactor.hpp"
#include <sstream>
#include <exception>

class DummyStream {
public:
    std::string str = "not a pdf";
    std::string read() { return str; }
    void close() {}
};

TEST(TestRedactorError, PdfParseError) {
    pdf_redactor::RedactorOptions opts;
    DummyStream input;
    std::ostringstream output;
    opts.input_stream = &input;
    opts.output_stream = &output;
    // Should throw exception (simulate invalid PDF input)
    try {
        pdf_redactor::redactor(opts);
        FAIL() << "Exception not raised on invalid PDF input";
    } catch (const std::exception& e) {
        SUCCEED();
    } catch (...) {
        SUCCEED();
    }
}