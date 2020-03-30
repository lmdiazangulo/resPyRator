/******************************************************************************************************************
*******************************************************************************************************************
*******************************************************************************************************************
SerialComDisplayPlus.h
*******************************************************************************************************************
*******************************************************************************************************************
******************************************************************************************************************/

#ifndef SERIALCOMDISPLAYPLUS_H
#define SERIALCOMDISPLAYPLUS_H

/*****************************************************************************************************************/
//Included headers
#include "Utilities.h"

#include <stdio.h>

/*****************************************************************************************************************/
//Definitions and macros

//Definitions for UART0 hardware
#define UART_PORT_DDR		DDRE
#define UART_PRR			PRR0
#define UART_PRUSART		PRUSART0
#define UART_RXCIE			RXCIE0
#define UART_RXEN			RXEN0
#define UART_TXEN			TXEN0
#define UART_U2X			U2X0
#define UART_UBRRH			UBRR0H
#define UART_UBRRL			UBRR0L
#define UART_UCSRA			UCSR0A
#define UART_UCSRB			UCSR0B
#define UART_UCSRC			UCSR0C
#define UART_UCSZ0			UCSZ00
#define UART_UDRE			UDRE0
#define UART_UDRIE			UDRIE0
#define UART_UMSEL0		UMSEL00
#define UART_USBS			USBS0

#define USART_RX_INT_vect		USART0_RX_vect
#define USART_UDRE_INT_vect	USART0_UDRE_vect

/*****************************************************************************************************************/
//Type and Structure declaration
typedef union {
    uint8_t uint8_val;
    int8_t int8_val;
} frame_8_t;

typedef union {
    uint32_t uint32_val;
    int32_t int32_val;
    
    struct {
      uint8_t high_byte;
      uint8_t mid_byte;
      uint8_t low_byte;
      uint8_t not_used;
    } bytes;

    struct {
      uint8_t byte_array[3];
      uint8_t not_used;
    } array;
} frame_24_t;

typedef union {
    uint16_t uint16_val;
    int16_t int16_val;
    
    struct {
      uint8_t high_byte;
      uint8_t low_byte;
    };
} frame_16_t;

typedef union {
  uint8_t byte_array[41];
  struct {
    uint8_t Header;
    uint8_t Protocol_version;
    frame_24_t UUID;
    frame_24_t TAG;
    frame_16_t RPM_setting;
    frame_16_t RPM_measure;
    frame_16_t PEAK_pressure_setting;
    frame_16_t PEAK_pressure_measure;
    frame_16_t PEEP_pressure_setting;
    frame_16_t PEEP_pressure_measure;
    frame_16_t TriggerFlow_setting;
    frame_16_t Flow_measure;
    frame_16_t Ramp_setting;
    uint8_t ActiveAlarmCode;
    uint8_t StatusBitField;
    frame_16_t TempValueEnc1;
    frame_16_t TempValueEnc2;
    frame_16_t TempValueEnc3;
    frame_16_t TempValueEnc4;
    frame_16_t Answer;
    uint8_t Answer_to_frame_number;
    frame_16_t Crc;
  } fields;
} tx_frame_t;

typedef union {
  uint8_t byte_array[8];
  struct {
    uint8_t Header;
    uint8_t Protocol_version;
    uint8_t Frame_number;
    uint8_t Command;
    frame_16_t Value;
    frame_16_t Crc;
  } fields;
} rx_frame_t;

/*****************************************************************************************************************/
//Global variable declaration

  extern ring_buffer_t UART_TX;
  extern ring_buffer_t UART_RX;
  extern tx_frame_t packet_tx;
  extern rx_frame_t packet_rx;

/*****************************************************************************************************************/
//Function declaration
void initSerialComDisplayPlus();
uint16_t CRC16(uint8_t *nData, uint16_t length);
void sendFrame(object serialPort);
void processReceivedData();

//void print_packet(tx_frame_t packet);

#endif