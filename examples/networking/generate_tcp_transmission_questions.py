#!/usr/bin/env python3
"""Generate questions about TCP header values when opening connections,
exchanging data and closing connections. For importing from Moodle.

Created for class "104353 Computer networks and internet" at the
Universitat Autònoma de Barcelona (UAB).
"""
__author__ = "Miguel Hernández-Cabronero"
__since__ = "2024/04/26"

import os
import textwrap
from typing import List
import dataclasses
import builtins
import random
import itertools
import moocloze

# If True, additional info is printed in the questions to simplify verification
DEBUG = False


@dataclasses.dataclass
class TCPMessage:
    SYN: int
    ACK: int
    FIN: int
    seq_number: int
    ack_number: int
    data_length: int
    source_ip: str
    source_port: int
    destination_ip: str
    destination_port: int
    hidden_fields: List[str]

    def to_table_row(self) -> str:
        field_names = [f.name for f in dataclasses.fields(self)]
        if self.hidden_fields:
            for f in self.hidden_fields:
                if f not in field_names:
                    raise ValueError(f"Found invalid hidden field {f!r}")

        s = "<tr>\n"
        for field in dataclasses.fields(self):
            if field.name == "hidden_fields":
                continue
            s += "\t<td>"
            if DEBUG:
                s += field.name + ": "
            if self.hidden_fields and field.name in self.hidden_fields:
                match field.type:
                    case builtins.int:
                        # print(f"{field.name=}")
                        # print(f"{field.type=}")
                        s += str(moocloze.Numerical(getattr(self, field.name)))
                    case builtins.str:
                        s += str(moocloze.ShortAnswer(getattr(self, field.name)))
                    case _:
                        raise ValueError(f"{field!s} not supported")
            else:
                if field.name == "ack_number" and self.ACK == 0:
                    s += "-"
                else:
                    s += str(getattr(self, field.name))
            s += "</td>\n"
        s += "</tr>\n"
        return s

    def to_table_header(self) -> str:
        return ("<tr>"
                + "".join(f"<th>{field.name}</th>" for field in dataclasses.fields(self)
                          if field.name != "hidden_fields")
                + "</tr>")


@dataclasses.dataclass
class TCPSequence:
    TCPmessages: List[TCPMessage]

    table_explanation: str = textwrap.dedent("""\
        Note that:
            <ul>
            <li><em>ACK</em>, <em>SYN</em>, <em>FIN</em> are binary flags with value 0 or 1.</li>
            <li><em>ack_number</em> and <em>seq_number</em> indicate the ACK and sequence numbers 
                in the segment header.</li>
            <li><em>data_length</em> is the number of <strong>data</strong> bytes 
                in the segment.</li>
            </ul> 
        """)

    def to_table(self) -> str:
        return ("<table>"
                + self.TCPmessages[0].to_table_header()
                + "".join(msg.to_table_row() for msg in self.TCPmessages)
                + "</table>")


def generate_transmission_no_errors(
        open_connection_questions_path=os.path.join(
            os.path.dirname(__file__), "open_connection_questions_no_error.xml"),
        data_exchange_a_path=os.path.join(
            os.path.dirname(__file__), "data_exchange_a_questions_no_piggyback_no_error.xml"),
        data_exchange_b_path=os.path.join(
            os.path.dirname(__file__), "data_exchange_b_questions_yes_piggyback_no_error.xml"),
        close_connection_questions_path=os.path.join(
            os.path.dirname(__file__), "close_connection_questions_no_error.xml")):
    open_connection_questions = []
    data_exchange_a_questions = []
    data_exchange_b_questions = []
    close_connection_questions = []

    open_question_index = itertools.count(1)
    exchange_question_a_index = itertools.count(1)
    exchange_question_b_index = itertools.count(1)
    close_question_index = itertools.count(1)

    for initial_sequence_a in [0, 555, 2 ** 32 - 7]:
        for initial_sequence_b in [13, 612, 2 ** 32 - 30]:
            ip_a, port_a = "192.168.1.3", random.randint(10000, 65000)
            ip_b, port_b = "192.168.1.6", random.choice([22, 80, 443, 8080])

            connection_messages = []
            connection_messages.append(TCPMessage(
                SYN=1, ACK=0, FIN=0, data_length=0,
                seq_number=initial_sequence_a, ack_number=None,
                source_ip=ip_a, source_port=port_a,
                destination_ip=ip_b, destination_port=port_b,
                hidden_fields=["SYN", "ACK", "FIN",
                               "source_ip", "source_port"]))
            connection_messages.append(TCPMessage(
                SYN=1, ACK=1, FIN=0, data_length=0,
                seq_number=initial_sequence_b,
                ack_number=(initial_sequence_a + 1) % (2 ** 32),
                source_ip=ip_b, source_port=port_b,
                destination_ip=ip_a, destination_port=port_a,
                hidden_fields=["SYN", "ACK", "FIN", "ack_number",
                               "source_ip", "source_port"]))
            connection_messages.append(TCPMessage(
                SYN=0, ACK=1, FIN=0, data_length=0,
                seq_number=(initial_sequence_a + 1) % (2 ** 32),
                ack_number=(initial_sequence_b + 1) % (2 ** 32),
                source_ip=ip_a, source_port=port_a,
                destination_ip=ip_b, destination_port=port_b,
                hidden_fields=["SYN", "ACK", "FIN",
                               "source_ip", "source_port",
                               "destination_ip", "destination_port",
                               "seq_number", "ack_number"]))

            open_connection_questions.append(moocloze.Question(
                name=f"Active opening of a TCP connection :: question {next(open_question_index)}",
                contents=textwrap.dedent(f"""\
                    <p>Complete the fields of the following table describing the 
                    exchanged segments that result in an active opening
                    of a TCP connection.<br/> 
                    {TCPSequence.table_explanation}<br/> 
                    Assume that no segment is lost and all hosts behave as expected.<p>
                    <p>{TCPSequence(connection_messages).to_table()}</p>                       
                    """),
                general_feedback=
                "It is very important to remember the values of the SYN and ACK flags,"
                "as well as how the sequence and ack numbers are incremented "
                "during the active TCP connection opening.",
            ))

            # The connection part is shown when asking about the data exchange
            for message in connection_messages:
                message.hidden_fields = []

            # A sends a full window, B sends no data (data_exchange_a_questions)
            for window_bytes in [200, 500, 1000]:
                for mss in [window_bytes // 2 - 3,
                            window_bytes // 3 - 4,
                            window_bytes // 4 - 5,
                            window_bytes // 5 - 7]:
                    sent_messages = []
                    received_messages = []

                    seq_a = (initial_sequence_a + 1) % (2 ** 32)
                    seq_b = (initial_sequence_b + 1) % (2 ** 32)

                    # B sends a full window of data to A - all the ACKs arrive afterwards
                    sent_data = 0
                    while sent_data < window_bytes:
                        segment_data_bytes = min(mss, window_bytes - sent_data)
                        sent_messages.append(TCPMessage(
                            SYN=0, ACK=1, FIN=0,
                            seq_number=seq_b, ack_number=seq_a,
                            data_length=segment_data_bytes,
                            source_ip=ip_b, source_port=port_b,
                            destination_ip=ip_a, destination_port=port_a,
                            hidden_fields=[
                                "SYN", "ACK", "destination_ip", "source_port", "destination_port",
                                "seq_number", "ack_number"],
                        ))
                        seq_b = (seq_b + segment_data_bytes) % (2 ** 32)
                        sent_data += segment_data_bytes

                        # A acknowledges the window
                        received_messages.append(TCPMessage(
                            SYN=0, ACK=1, FIN=0,
                            seq_number=seq_a, ack_number=seq_b,
                            source_ip=ip_a, source_port=port_a,
                            destination_ip=ip_b, destination_port=port_b,
                            data_length=0, hidden_fields=[
                                "SYN", "ACK", "destination_ip", "source_port", "destination_port",
                                "seq_number", "ack_number"],
                        ))

                    data_exchange_a_questions.append(moocloze.Question(
                        name=f"TCP data exchange A :: question {next(exchange_question_a_index)}",
                        contents=textwrap.dedent(f"""\
                        <p>Complete the fields of the following table describing the 
                        exchanged segments between two hosts.<br/> 
                        {TCPSequence.table_explanation}<br/> 
                        Assume that:
                         <ul>
                         <li>No segment is lost and all hosts behave as expected.</li>
                         <li>Segments arrive and are sent in order.</li>
                         <li>Only two endpoints are involved.</li>
                         <li>ACKs are sent for each received segment whenever it is needed.</li>
                         </ul>
                        
                        <p>Once you complete the table, indicate the most likely values for 
                        these parameters:
                        <ul>
                        <li>MSS (bytes): {moocloze.Numerical(mss)}</li>
                        <li>Window size (bytes): {moocloze.Numerical(window_bytes)}</li>
                        </ul>
                        </p>
                                                
                        <p>{TCPSequence(connection_messages + sent_messages + received_messages).to_table()}</p>                       
                        """),
                        general_feedback=""
                    ))

            # A and B send data and piggyback
            for _ in range(10):
                data_a1_bytes = random.randint(1, 400)
                data_b1_bytes = random.randint(10, 200)
                data_a2_bytes = random.randint(3, 300)
                data_b2_bytes = random.randint(55, 600)

                seq_a = (initial_sequence_a + 1) % (2 ** 32)
                seq_b = (initial_sequence_b + 1) % (2 ** 32)

                data_exchange_messages = []
                # A -> B (data_a1_bytes)
                data_exchange_messages.append(TCPMessage(
                    source_ip=ip_a, source_port=port_a,
                    destination_ip=ip_b, destination_port=port_b,
                    SYN=0, ACK=1, FIN=0,
                    seq_number=seq_a, ack_number=seq_b,
                    data_length=data_a1_bytes,
                    hidden_fields=["ACK", "SYN",
                                   "source_port", "destination_ip", "destination_port",
                                   "seq_number", "ack_number", "data_length"],
                ))
                seq_a = (seq_a + data_a1_bytes) % (2 ** 32)
                # B -> A
                data_exchange_messages.append(TCPMessage(
                    source_ip=ip_b, source_port=port_b,
                    destination_ip=ip_a, destination_port=port_a,
                    SYN=0, ACK=1, FIN=0,
                    seq_number=seq_b, ack_number=seq_a,
                    data_length=data_b1_bytes,
                    hidden_fields=["ACK", "SYN",
                                   "source_ip", "destination_ip", "destination_port",
                                   "seq_number", ],
                ))
                seq_b = (seq_b + data_b1_bytes) % (2 ** 32)
                # A -> B
                data_exchange_messages.append(TCPMessage(
                    source_ip=ip_a, source_port=port_a,
                    destination_ip=ip_b, destination_port=port_b,
                    SYN=0, ACK=1, FIN=0,
                    seq_number=seq_a, ack_number=seq_b,
                    data_length=data_a2_bytes,
                    hidden_fields=["ACK", "SYN",
                                   "seq_number", "ack_number",
                                   "source_port", "destination_ip"],
                ))
                seq_a = (seq_a + data_a2_bytes) % (2 ** 32)
                # B -> A
                data_exchange_messages.append(TCPMessage(
                    source_ip=ip_b, source_port=port_b,
                    destination_ip=ip_a, destination_port=port_a,
                    SYN=0, ACK=1, FIN=0,
                    seq_number=seq_b, ack_number=seq_a,
                    data_length=data_b2_bytes,
                    hidden_fields=["ACK", "SYN",
                                   "source_ip", "destination_ip", "destination_port",
                                   "seq_number", "ack_number"],
                ))
                seq_b = (seq_b + data_b2_bytes) % (2 ** 32)
                # Final ACK
                data_exchange_messages.append(TCPMessage(
                    source_ip=ip_a, source_port=port_a,
                    destination_ip=ip_b, destination_port=port_b,
                    SYN=0, ACK=1, FIN=0,
                    seq_number=seq_a, ack_number=seq_b,
                    data_length=0,
                    hidden_fields=["ACK", "SYN", "seq_number", "ack_number",
                                   "source_ip", "source_port", "destination_ip"],
                ))

                data_exchange_b_questions.append(moocloze.Question(
                    name=f"TCP data exchange B :: question {next(exchange_question_b_index)}",
                    contents=textwrap.dedent(f"""\
                    <p>Complete the fields of the following table describing the 
                    exchanged segments between two hosts.<br/> 
                    {TCPSequence.table_explanation}<br/> 
                    Assume that:
                     <ul>
                     <li>No segment is lost and all hosts behave as expected.</li>
                     <li>Segments arrive and are sent in order.</li>
                     <li>Only two endpoints are involved.</li>
                     <li>ACKs are sent for each received segment whenever it is needed.</li>
                     <li>When a segment is sent, it is received by the other endpoint before 
                         the next segment (from either side) is sent.</li>
                     </ul>
                    
                    <p>{TCPSequence(connection_messages + data_exchange_messages).to_table()}</p>
                    """),
                    general_feedback="Don't forget about piggybacking."
                ))

                # Add closing questions
                for m in data_exchange_messages:
                    m.hidden_fields = []

                # A closes
                close_connection_messages = []
                # FIN A->B
                close_connection_messages.append(TCPMessage(
                    source_ip=ip_a, source_port=port_a,
                    destination_ip=ip_b, destination_port=port_b,
                    SYN=0, ACK=1, FIN=1,
                    seq_number=seq_a, ack_number=seq_b, data_length=0,
                    hidden_fields=["SYN", "ACK", "FIN"],
                ))
                seq_a = (seq_a + 1) % (2 ** 32)
                # FIN, ACK B->A
                close_connection_messages.append(TCPMessage(
                    source_ip=ip_b, source_port=port_b,
                    destination_ip=ip_a, destination_port=port_a,
                    SYN=0, ACK=1, FIN=1,
                    seq_number=seq_b, ack_number=seq_a, data_length=0,
                    hidden_fields=["SYN", "ACK", "FIN",
                                   "seq_number", "ack_number",],
                ))
                seq_b = (seq_b + 1) % (2 ** 32)
                # ACK A->B
                close_connection_messages.append(TCPMessage(
                    source_ip=ip_a, source_port=port_a,
                    destination_ip=ip_b, destination_port=port_b,
                    SYN=0, ACK=1, FIN=0,
                    seq_number=seq_a, ack_number=seq_b, data_length=0,
                    hidden_fields=["SYN", "ACK", "FIN",
                                   "seq_number", "ack_number",],
                ))

                close_connection_questions.append(moocloze.Question(
                    name=f"TCP close connection :: question {next(close_question_index)}",
                    contents=textwrap.dedent(f"""\
                    <p>Complete the fields of the following table describing the 
                    exchanged segments that result in a "polite" <strong>closing</strong>
                    of a TCP connection.<br/> 
                    {TCPSequence.table_explanation}<br/>
                     
                    Assume that:
                    <ul>
                    <li>No segment is lost</li>
                    <li>All hosts behave as expected.</li>
                    <li>No RST segment is sent.</li>
                    </ul>
                    </p>
                    
                    <p>{TCPSequence(connection_messages + data_exchange_messages + close_connection_messages).to_table()}</p> 
                    """)
                ))

    moocloze.questions_to_xml_file(questions=open_connection_questions,
                                   output_path=open_connection_questions_path)
    moocloze.questions_to_xml_file(questions=data_exchange_a_questions,
                                   output_path=data_exchange_a_path)
    moocloze.questions_to_xml_file(questions=data_exchange_b_questions,
                                   output_path=data_exchange_b_path)
    moocloze.questions_to_xml_file(questions=close_connection_questions,
                                   output_path=close_connection_questions_path)


if __name__ == "__main__":
    generate_transmission_no_errors()
