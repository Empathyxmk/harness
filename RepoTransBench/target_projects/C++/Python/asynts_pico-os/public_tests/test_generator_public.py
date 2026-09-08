import pytest

class Generator:
    class Section:
        def __init__(self, name, sht, flags):
            self.name = name
            self.sht = sht
            self.flags = flags
    class Symtab:
        def __init__(self):
            self.symbols = []
        def add_symbol(self, name, sym):
            idx = len(self.symbols)
            self.symbols.append((name, sym))
            return idx
    SHT_PROGBITS = 1
    SHF_ALLOC = 0x2
    SHF_WRITE = 0x1
    def __init__(self):
        self.sections = []
        self.symtab_inst = Generator.Symtab()
    def create_section(self, name, sht, flags):
        idx = len(self.sections)
        self.sections.append(self.Section(name, sht, flags))
        return idx
    def symtab(self):
        return self.symtab_inst

def ELF32_ST_INFO(bind, typ):
    # Dummy (return as int for test)
    return (bind << 4) | typ

STB_LOCAL = 0
STT_OBJECT = 1
STV_DEFAULT = 0

def test_section_creation_different():
    gen = Generator()
    data_idx = gen.create_section(".data_public", Generator.SHT_PROGBITS, Generator.SHF_ALLOC|Generator.SHF_WRITE)
    rodata_idx = gen.create_section(".rodata_public", Generator.SHT_PROGBITS, Generator.SHF_ALLOC)
    assert data_idx != rodata_idx

def test_symbol_table_different():
    gen = Generator()
    idx_a = gen.create_section(".a_public", Generator.SHT_PROGBITS, Generator.SHF_ALLOC)
    class Sym: pass
    sym = Sym()
    sym.st_value = 456
    sym.st_size = 4
    sym.st_info = ELF32_ST_INFO(STB_LOCAL, STT_OBJECT)
    sym.st_other = STV_DEFAULT
    sym.st_shndx = idx_a
    index = gen.symtab().add_symbol("foo_public", sym)
    assert index >= 0