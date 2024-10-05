import { render, screen, fireEvent } from '@testing-library/react';
import App from '../App';
import useStepTime from '../useStepTime';
import { act } from 'react';
import WS from 'jest-websocket-mock';

jest.mock('../useStepTime');

test('Step Time Component is rendered on screen', () => {
  useStepTime.mockReturnValue({
    left: 0,
    right: 0,
    targetZones: {
      left: { min: 25, max: 30 },
      right: { min: 50, max: 45 }
    }
  });
  
  render(<App />);
  expect(screen.getByTestId('step-time-digits-view')).toBeInTheDocument();
});

describe('Navbar Component', () => {
  beforeEach(() => {
    useStepTime.mockReturnValue({
      left: 0,
      right: 0,
      targetZones: {
        left: { min: 25, max: 30 },
        right: { min: 50, max: 45 }
      } 
    });
  });

  test('Navbar is rendered on screen', () => {
    render(<App />);
    expect(screen.getByRole('navigation')).toBeInTheDocument();
  });

  describe('View Swapping', () => {
    test('Navbar swap renders StepTimeChart view', () => {
      render(<App />);
      fireEvent.click(screen.getByTestId('step-time-chart-nav'));
      expect(screen.getByTestId('step-time-chart-view')).toBeInTheDocument();
    });
  
    test('Navbar swap renders StepTimeGraph view', () => {
      render(<App />);
      fireEvent.click(screen.getByTestId('step-time-graph-nav'));
      expect(screen.getByTestId('step-time-graph-view')).toBeInTheDocument();
    });
  
    test('Navbar swap renders StepTimeDigits view', () => {
      render(<App />);
      fireEvent.click(screen.getByTestId('step-time-graph-nav'));
      fireEvent.click(screen.getByTestId('step-time-digits-nav'));
      expect(screen.getByTestId('step-time-digits-view')).toBeInTheDocument();
    });
  });
});

describe('WebSocket in App Component', () => {
  let server;

  beforeEach(() => {
    server = new WS("ws://localhost:8000/ws");
    
    useStepTime.mockReturnValue({
      left: 0,
      right: 0,
      targetZones: {
        left: { min: 25, max: 30 },
        right: { min: 50, max: 45 }
      } 
    });
  });

  afterEach(() => {
    WS.clean();
  });

  test('WebSocket connection messages', async () => {
    const consoleLogSpy = jest.spyOn(console, 'log');

    await act(async () => {
      render(<App />);
    });

    await server.connected;

    server.send("Message from backend");

    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 100));
    });

    expect(consoleLogSpy).toHaveBeenCalledWith("Data received from backend: ", "Message from backend");

    consoleLogSpy.mockRestore();
  });

  test('Message on WebSocket connection open', async () => {
    await act(async () => {
      render(<App />);
    });

    await server.connected;

    expect(server).toReceiveMessage("Websocket Connected to React");
  });
});