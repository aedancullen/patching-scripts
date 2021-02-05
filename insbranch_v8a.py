import sys
import struct

# Tool for patching in unconditional branch instructions to ARMv8-A binaries

B = 0b00010100000000000000000000000000
B_tc_mask = 0b00000011111111111111111111111111

if __name__ == "__main__":
    filename = sys.argv[1]
    instr_offset = int(sys.argv[2], 16)
    branch_offset = int(sys.argv[3], 16)
    with open(filename, "rb") as file:
        file.seek(instr_offset, 0)
        instr_bytes = int.from_bytes(file.read(4), "little")
        file.seek(branch_offset, 0)
        branch_bytes = int.from_bytes(file.read(4), "little")
    print("Instruction offset:\t", format(instr_offset, 'X'), "\tcurrent bytes", format(instr_bytes, 'X'))
    print("Destination offset:\t", format(branch_offset, 'X'), "\tcurrent bytes", format(branch_bytes, 'X'))
    packed_tc = int.from_bytes(struct.pack("<i", branch_offset - instr_offset), "little")
    packed_tc >>= 2
    new_instr = B | (B_tc_mask & packed_tc)
    print("\nNew instruction:\t", format(new_instr, 'X'))
    print("\nConfirm? <ENTER>")
    input()
    with open(filename, "r+b") as file:
        file.seek(instr_offset, 0)
        file.write(new_instr.to_bytes(4, "little"))
    print("Done")
 
